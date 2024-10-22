from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem
from app.deps import engine





#update inventory stock when payment is succeeded
def update_stock_in_inventory(order_data):
    with Session(engine) as session:
        inventory = session.exec(select(InventoryItem).where(InventoryItem.product_id == order_data["product_id"])).one_or_none()
        if inventory:
            inventory.quantity -= order_data["quantity"]
            session.add(inventory)
            session.commit()
            session.refresh(inventory)
            print(f"Updated inventory for product_id {order_data['product_id']}: new stock is {inventory.quantity}")
        else:
            print(f"No inventory found for product_id {order_data['product_id']}")