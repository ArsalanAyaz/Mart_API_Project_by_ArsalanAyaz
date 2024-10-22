# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated,Any
from sqlmodel import Field, Session, SQLModel, select, Sequence # type: ignore
from fastapi import FastAPI, Depends,HTTPException # type: ignore
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer #type:ignore
import asyncio
import json
from app import settings
from app.db_engine import engine
from app.deps import get_kafka_producer,get_session
from app.models.order_model import Order,OrderUpdate,OrderBase,OrderCreate,OrderRead
from app.crud.order_cruds import place_order,get_all_orders,get_order,delete_order,send_order_to_kafka,get_product_price,update_order_status
import requests
from app.consumer.order_check_reponse import consume_order_response_messages
from app.consumer.order_status_update import consume_payment_response_message
from app.shared_auth import get_current_user,get_login_for_access_token,admin_required,oauth2_scheme

GetCurrentUserDep = Annotated[ Any, Depends(get_current_user)]
LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables...")
    #listens the order-check-response topic
    task = asyncio.create_task(consume_order_response_messages("order-check-response", settings.BOOTSTRAP_SERVER))
    asyncio.create_task(consume_payment_response_message("payment_succeeded", settings.BOOTSTRAP_SERVER))
    create_db_and_tables()
    yield 


app = FastAPI(lifespan=lifespan,
            title="Order API with DB", 
            version="0.0.1"
            )

            
@app.get("/")
def read_root():
    return {"Welcome": "order_service"}


@app.post("/auth/login")
def login(token:LoginForAccessTokenDep):
    return token


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)], current_user: GetCurrentUserDep):
    # Check if the current user is an admin
    if current_user['role'] == 'admin':
        raise HTTPException(status_code=403, detail="Admins are not allowed to place orders")

    product_price = get_product_price(order.product_id, token=current_user['access_token'])
    # product_price = get_product_price(order.product_id)
    # print("Product Price:", product_price)

    order_data = Order(**order.dict(exclude={"user_id"}), user_id=current_user["id"])
    new_order = send_order_to_kafka(session, order_data, product_price)

    # send order to kafka topic 
    order_dict = {field: getattr(order_data, field) for field in new_order.dict()}
    order_json = json.dumps(order_dict).encode("utf-8")
    print("orderJSON:", order_json)
    
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_json)

    # Create notification message
    notification_message = {
        "user_id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "title": "Order Created",
        "message": f"Order ID {new_order.id} has been successfully created by {current_user['username']}.",
        "recipient": current_user["email"],
        "status": "pending"
    }
    notification_json = json.dumps(notification_message).encode("utf-8")
    await producer.send_and_wait(settings.KAFKA_NOTIFICATION_TOPIC, notification_json)

    return new_order

# @app.get("/orders/{order_id}", response_model=OrderRead)
# def read_order(order_id: int, session: Session = Depends(get_session), current_user: Any = Depends(get_current_user)):
#     return get_order(session, order_id, current_user["id"])

@app.get("/orders/", response_model=list[OrderRead])
def list_orders(session: Session = Depends(get_session), current_user: Any = Depends(admin_required)):
    return get_all_orders(session)


@app.delete("/orders/{order_id}")
def delete_order_by_id(order_id: int, session: Annotated[Session, Depends(get_session)], current_user: Any = Depends(admin_required)):
    return delete_order(session=session, order_id=order_id)
        
@app.patch("/orders/{order_id}", response_model=Order)
def update_status(order_id: int, status: str, session: Annotated[Session, Depends(get_session)], current_user: Any = Depends(admin_required)):
    order = update_order_status(session, order_id, status)
    # # Create notification message
    # notification_message = {
    #     "user_id": current_user["id"],
    #     "username": current_user["username"],
    #     "email": current_user["email"],
    #     "title": "Order Created",
    #     "message": f"Order ID {new_order.id} has been successfully created by {current_user['username']}.",
    #     "recipient": current_user["email"],
    #     "status": "pending"
    # }
    # notification_json = json.dumps(notification_message).encode("utf-8")
    # await producer.send_and_wait("notification-topic", notification_json)

    return order


@app.get("/my-orders/", response_model=list[Order])
async def read_my_orders(current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    """Retrieve all orders for the currently authenticated user"""
    user_id = current_user['id']
    orders = session.exec(select(Order).where(Order.user_id == user_id)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders