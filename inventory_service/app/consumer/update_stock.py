from aiokafka import AIOKafkaConsumer
import json
from app.deps import get_session
from app.stock_update import update_stock_in_inventory

#this is the consumer of topic {product-events} which consumes the product which is going to be add 


async def consume_order_paid_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="update-stock-consumer-group",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for msg in consumer:
            order_data = json.loads(msg.value.decode())
            print(f"Received order paid event: {order_data}")
            update_stock_in_inventory(order_data)
    finally:
        await consumer.stop()
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.


# if __name__ == "__main__":
#     import asyncio
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(consume_order_paid_messages())            