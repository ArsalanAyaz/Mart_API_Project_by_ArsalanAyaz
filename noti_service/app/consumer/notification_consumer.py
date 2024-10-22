from contextlib import asynccontextmanager
from app.send_email import send_email_notification
from sqlmodel import Field, Session, SQLModel, select, Sequence
from fastapi import FastAPI, Depends,HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json
from app.deps import get_session
from app.db_engine import engine
from app.models.noti_models import Notification
from app.crud.noti_crud import add_new_notification









async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="notification-consumer-group",
        #auto_offset_reset="earliest",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            notification_data = json.loads(message.value.decode())
            print(f"Notification Data: {notification_data}")

            with next(get_session()) as session:
                print("Saving data to database")
                db_insert_notification = add_new_notification(
                    notification_data=Notification(**notification_data), session=session)
                print("DB_INSERT_NOTIFICATION", db_insert_notification)
            #Send email notification
            if 'recipient' in notification_data:
                    send_email_notification(
                        email_to=notification_data['recipient'],
                        subject=notification_data['title'],
                        email_content_for_send=notification_data['message']
                    )
    finally:
        
        await consumer.stop()
