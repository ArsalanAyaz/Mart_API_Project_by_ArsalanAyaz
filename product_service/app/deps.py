from sqlmodel import Session
from app.db_engine import engine
from aiokafka import AIOKafkaProducer
from app import settings


def get_session():
    with Session(engine) as session:
        yield session

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=settings.BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()        