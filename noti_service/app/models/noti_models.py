from sqlmodel import SQLModel,Field
from typing import Optional


class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    title: str
    message: str
    recipient: str
    status: str
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # sent_at: Optional[datetime] = None

class NotificationUpdate(SQLModel):
    user_id: int
    title: Optional[str] = None
    message: Optional[str] = None
    recipient: Optional[str] = None
    status: Optional[str] = None
    # sent_at: Optional[datetime] = None

