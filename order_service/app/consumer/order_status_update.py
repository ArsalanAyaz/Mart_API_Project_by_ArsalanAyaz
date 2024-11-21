from aiokafka import AIOKafkaConsumer #type:ignore
import json
from app.deps import get_session
from app.payment_processing import process_payment_event
from app.models.order_model import Order
from app.deps import get_kafka_producer

# this consumer listens order-check-response topic 
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



# async def consume_payment_response_message(topic, bootstrap_servers):
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id="order-status-update-group",
#         auto_offset_reset="earliest",
#     )

#     await consumer.start()
#     try:
#         async for message in consumer:
#             print(f"Received message on topic {message.topic}")
#             payment_data = json.loads(message.value.decode())
#             print(f"Received payment event: {payment_data}")
            
#             # Ensure the payment data contains the required fields
#             order_id = payment_data.get('order_id')
#             status = payment_data.get('status')
            
#             if status == "Paid":
#                 session = next(get_session())
#                 try:
#                     order = session.exec(select(Order).where(Order.id == order_id)).one_or_none()
#                     if order:
#                         order.status = "Paid"
#                         session.add(order)
#                         session.commit()
#                         session.refresh(order)
#                         print(f"Order {order_id} status updated to 'Paid'")
#                     else:
#                         print(f"Order {order_id} not found")
#                 except Exception as e:
#                     session.rollback()
#                     print(f"Failed to update order status: {e}")
#                 finally:
#                     session.close()
#     finally:
#         await consumer.stop()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_payment_response_message())        