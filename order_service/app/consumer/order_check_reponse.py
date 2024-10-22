from aiokafka import AIOKafkaConsumer #type:ignore
import json
from app.deps import get_session
from app.crud.order_cruds import place_order,get_product_price
from app.models.order_model import Order
from app.deps import get_kafka_producer

#this consumer listens order-check-response topic 
# if the status = success then allow user to place order otherwise raise error

async def consume_order_response_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-check-response-group",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("RAW CHECK RESPONSE CONSUMER MESSAGE")
            print(f"Received message on topic {message.topic}")

            response_data = json.loads(message.value.decode())
            # print("TYPE", (type(inventory_data)))
            print(f"Response Data {response_data}")
                #Ganlde insufficient stock
            if response_data["status"] == "success":
                # Proceed with placing the order
                session = next(get_session())
                try:
                    order_data = response_data["order"]
                    # token = response_data["token"]
                    # product_price = get_product_price(order_data["product_id"],token)
                    new_order = place_order(session, Order(**order_data))
                    print(f"Order placed successfully")
                except Exception as e:
                    session.rollback()  # Rollback in case of error
                    print(f"Failed to place order: {e}")
                finally:
                    session.close()
                # order_data = response_data["order"]
                # product_price = get_product_price(order_data["product_id"])
                # new_order = place_order(session, Order(**order_data), product_price)
                # print(f"Order placed successfully")
            else:
                # Handle insufficient stock
                print(f"Insufficient stock for order: {response_data['order_id']}")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()