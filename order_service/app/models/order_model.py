from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional






class OrderBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    # user_id: int
    quantity: int
    # total_price: float
    status: str = Field(default="Unpaid")

class Order(OrderBase, table=True):
    total_price: float
    user_id: int
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    total_price: float
    user_id: int
    # created_at: datetime
    # updated_at: datetime

class OrderUpdate(SQLModel):
    product_id: Optional[int] = None
    user_id: Optional[int] = None
    quantity: Optional[int] = None
    total_price: Optional[int] = None
    status: Optional[str] = None














# class Order(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     product_id: int
#     user_id: int
#     total_price: float
#     quantity: int
#     status: str
#     # created_at: datetime = Field(default_factory=datetime.utcnow)
#     # updated_at: datetime = Field(default_factory=datetime.utcnow)

#     # items: list[OrderItem] = Relationship(back_populates="order")



# class UpdateOrder(SQLModel):
#     product_id: int
#     user_id: int
#     quantity: int
#     total_price: float
#     status: str
#     # created_at: datetime = Field(default_factory=datetime.utcnow)


