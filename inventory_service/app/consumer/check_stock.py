from aiokafka import AIOKafkaConsumer #type:ignore
import json
from sqlmodel import Session, select
from app.deps import get_session
from app.models.inventory_model import InventoryItem
from aiokafka import AIOKafkaProducer
from app.deps import get_kafka_producer
from typing import Annotated

#this is the consumer of topic {order_placed} which consumes the data which is placed 
# and the stock in inventory . if its ok then produce  success status event to new topic and is 
# its not then produce failed status event  



async def consume_order_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="check-inventory-stock",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            order_data = json.loads(message.value.decode())
            print("TYPE", (type(order_data)))
            print(f"Order Data {order_data}")

            with next(get_session()) as session:
                try:
                    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.product_id == order_data["product_id"])).one_or_none()
                    if inventory_item and inventory_item.quantity >= order_data["quantity"]:
                        # updated_stock = update_inventory_stock(session, order_data["product_id"], -order_data["quantity"])
                        response = {"order_id": order_data["id"], "status": "success", "order": order_data}
                        print("status : success")
                    else:
                    # Insufficient stock
                        response = {"order_id": order_data["id"], "status": "failed", "order": order_data}
                        print("status : failed")
                except Exception as e:
                    response = {"order_id": order_data["id"], "status": "error", "detail": str(e), "order": order_data}
                    
            response_json = json.dumps(response).encode("utf-8")
            producer = AIOKafkaProducer(
                        bootstrap_servers='broker:19092')
            await producer.start()
            try:
                await producer.send_and_wait(
                    "order-check-response",
                    response_json
                )
            finally:
                await producer.stop()
            # producer = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
            # response_json = json.dumps(response).encode("utf-8")
            # await producer.send_and_wait("order-check-response", response_json)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()