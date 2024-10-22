from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem,InventoryItemUpdate

# Add a New Inventory Item to the Database
def add_new_inventory_item(inventory_item_data: InventoryItem, session: Session):
    print("Adding Inventory Item to Database")
    session.add(inventory_item_data)
    session.commit()
    session.refresh(inventory_item_data)
    return inventory_item_data

# Get All Inventory Items from the Database
def get_all_inventory_items(session: Session):
    all_inventory_items = session.exec(select(InventoryItem)).all()
    return all_inventory_items

# Get an Inventory Item by ID
def get_inventory_item_by_id(inventory_item_id: int, session: Session):
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    return inventory_item

# Delete Inventory Item by ID
def delete_inventory_item_by_id(inventory_item_id: int, session: Session):
    # Step 1: Get the Inventory Item by ID
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    # Step 2: Delete the Inventory Item
    session.delete(inventory_item)
    session.commit()
    return {"message": "Inventory Item Deleted Successfully"}

# Update Inventory by Product ID
def update_inventory_by_id(product_id: int, update_product_inventory:InventoryItemUpdate, session: Session):
    # Step 1: Get the inventory by Product ID
    inventory = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id)).one_or_none()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Update the Product
    update_data = update_product_inventory.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inventory, key, value)
    session.add(inventory)
    session.commit()
    return inventory




# #update inventory stock
# def update_inventory_stock(session: Session, product_id: int, quantity_change: int):
#     inventory_item = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id)).one_or_none()
#     if inventory_item:
#         if inventory_item.quantity + quantity_change < 0:
#             raise HTTPException(status_code=400, detail="Insufficient stock")
#         inventory_item.quantity += quantity_change
#         session.add(inventory_item)
#         session.commit()
#         return inventory_item
#     else:
#         raise HTTPException(status_code=404, detail="Product not found")    


