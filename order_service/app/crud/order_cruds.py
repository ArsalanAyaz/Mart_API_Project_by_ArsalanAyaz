from sqlmodel import Session, select # type: ignore
from app.models.order_model import Order,OrderUpdate
from fastapi import HTTPException # type: ignore
import requests
from app.db_engine import engine
from aiokafka import AIOKafkaProducer #type:ignore
from app.consumer.order_status_update import consume_payment_response_message
import requests


def send_order_to_kafka(session: Session, order: Order, product_price: float):
    order.total_price = order.quantity * product_price  # Calculate total price
    return order

def place_order(session: Session, order: Order):  #product_price: float
    # order.total_price = order.quantity * product_price  # Calculate total price
    order.status = "Unpaid"  # Set default status to "Unpaid"
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order(session: Session, order_id: int) -> Order:
    order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return order

def get_all_orders(session: Session) -> list[Order]:
    statement = select(Order)
    return session.exec(statement).all()

# def update_order(session: Session, order_id: int, user_id: int, to_update_order: OrderUpdate) -> Order:
#     order = get_order(session, order_id, user_id)
#     hero_data = to_update_order.dict(exclude_unset=True)
#     for key, value in hero_data.items():
#         setattr(order, key, value)
#     session.add(order)
#     session.commit()
#     session.refresh(order)
#     return order


def update_order_status(session: Session, order_id: int, status: str):
    order = get_order(session, order_id)
    order.status = status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def delete_order(session: Session, order_id: int):
    order = get_order(session, order_id)
    session.delete(order)
    session.commit()
    return {"message": "Order deleted successfully"}



def get_product_price(product_id: int, token: str | None) -> float:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f'http://product-service-api:8003/products/{product_id}', headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch product price. Status code: {response.status_code}, Response: {response.text}")
    
    response_data = response.json()
    
    if 'price' not in response_data:
        raise HTTPException(status_code=404, detail="Product price not found")
    
    return response_data['price']

# def get_product_price(product_id: int) -> float:
#     # Fetch product price from Product Service
#     response = requests.get(f'http://product-service-api:8003/products/{product_id}')
#     response_data = response.json()
#     return response_data['price']
