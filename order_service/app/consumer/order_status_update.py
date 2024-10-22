from aiokafka import AIOKafkaConsumer #type:ignore
import json
from app.deps import get_session
from app.payment_processing import process_payment_event
from app.models.order_model import Order
from app.deps import get_kafka_producer

#this consumer listens order-check-response topic 
# if the status = success then allow user to place order otherwise raise error

async def consume_payment_response_message(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-status-update-group",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message on topic {message.topic}")
            payment_data = json.loads(message.value.decode())
            print(f"Received payment event: {payment_data}")
            await process_payment_event(payment_data)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_payment_response_message())        