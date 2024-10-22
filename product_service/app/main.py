# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from sqlmodel import Field, Session, SQLModel, select, Sequence
from fastapi import FastAPI, Depends,HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import asyncio
import json
from sqlmodel import create_engine
from app import settings
from app.db_engine import engine
from app.deps import get_kafka_producer,get_session
from app.models.product_model import Product,ProductUpdate
from app.crud.product_crud import get_all_products,delete_product_by_id,update_product_by_id,get_product_by_id
from app.consumer.product_consumer import consume_messages
from app.shared_auth import get_current_user,admin_required,LoginForAccessTokenDep,admin_user


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables......")
    task = asyncio.create_task(consume_messages(settings.KAFKA_ORDER_TOPIC, settings.BOOTSTRAP_SERVER))
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Product API with DB", 
    version="0.0.1",
    # servers=[
    #     {
    #         "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
    #         "description": "Development Server"
    #     }
    #     ]
        )



@app.get("/")
def read_root():
    return {"Product": "Service"}

@app.post("/auth/login")
def login(token:LoginForAccessTokenDep):
    return token

@app.post("/products/", response_model=Product,dependencies=[Depends(admin_required)])
async def create_new_product(product: Product, session: Annotated[Session, Depends(get_session)],producer:Annotated[AIOKafkaProducer,Depends(get_kafka_producer)]):
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("productJSON:", product_json)
    # # Produce message
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, product_json)
    # new_product = add_new_product(product,session)
    return product

@app.get("/products/", response_model=list[Product],dependencies=[Depends(get_current_user)])
def read_products(session: Annotated[Session, Depends(get_session)]):
    """ Get all products from the database"""
    return get_all_products(session)

@app.get("/products/{product_id}", response_model=Product,dependencies=[Depends(admin_user)])
def read_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """Read a single product"""
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e


@app.delete("/products/{product_id}",dependencies=[Depends(admin_required)])
def delete_products(product_id:int , session: Annotated[Session, Depends(get_session)]):
    """ Delete a single product by ID"""
    try:
        return delete_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/products/{product_id}", response_model=Product,dependencies=[Depends(admin_required)])
def update_single_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    """ Update a single product by ID"""
    try:
        return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))