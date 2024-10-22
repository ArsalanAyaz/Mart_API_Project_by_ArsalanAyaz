from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class Payment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int
    user_id: int
    username: str
    email : str
    amount: float
    currency: str = Field(default="usd")
    status: str
    method: str  # "cash_on_delivery" or "stripe"
    stripe_payment_intent_id: Optional[str] = None
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentCreate(SQLModel):
    order_id: int
    amount: float
    method: str  # "cash_on_delivery" or "stripe"

class PaymentUpdate(SQLModel):
    status: str
