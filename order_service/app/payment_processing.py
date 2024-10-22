from sqlmodel import Session, select # type: ignore
from app.models.order_model import Order
from fastapi import HTTPException # type: ignore
from app.db_engine import engine
from aiokafka import AIOKafkaProducer #type:ignore
import json
# from app.consumer.order_status_update import consume_payment_response_message




async def process_payment_event(payment_data):
    with Session(engine) as session:
        order = session.exec(select(Order).where(Order.id == payment_data["order_id"])).one_or_none()
        if order:
            order.status = "Paid"
            session.add(order)
            session.commit()
            session.refresh(order)
            # Produce event to update inventory
            event = {
                "order_id": order.id,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "status": "Paid"
            }
            await produce_event("order_paid", event)


async def produce_event(topic, event):
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        await producer.send_and_wait(topic, json.dumps(event).encode('utf-8'))
        print(f"Produced event to {topic}: {event}")
    finally:
        await producer.stop()           
            
# if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(consume_payment_response_message())
