from aiokafka import AIOKafkaConsumer
import json
from app.deps import get_session
from app.crud.inventory_crud import add_new_inventory_item
from app.models.inventory_model import InventoryItem

#this is the consumer of topic {product-events} which consumes the product which is going to be add 


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="add-inventory-consumer-group",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("RAW ADD STOCK CONSUMER MESSAGE")
            print(f"Received message on topic {message.topic}")

            inventory_data = json.loads(message.value.decode())
            print("TYPE", (type(inventory_data)))
            print(f"Inventory Data {inventory_data}")

            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                # inventory_item_data: InventoryItem
                db_insert_product = add_new_inventory_item(
                    inventory_item_data=InventoryItem(
                        product_id=inventory_data["id"],
                        quantity=inventory_data["quantity"],
                        name=inventory_data["name"]
                    ), 
                    session=session)
                
                print("DB_INSERT_STOCK", db_insert_product)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()