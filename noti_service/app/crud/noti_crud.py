from app.models.noti_models import Notification
from sqlmodel import Session , select
from fastapi import HTTPException
from app.models.noti_models import NotificationUpdate


# Add a New Notification to the Database
def add_new_notification(notification_data: Notification, session: Session):
    session.add(notification_data)
    session.commit()
    session.refresh(notification_data)
    return notification_data

# Get All Notifications from the Database
def get_all_notifications(session: Session):
    all_notifications = session.exec(select(Notification)).all()
    return all_notifications

# Get Notification by ID
def get_notification_by_id(notification_id: int, session: Session):
    notification = session.exec(select(Notification).where(Notification.id == notification_id)).one_or_none()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

# Delete Notification by ID
def delete_notification_by_id(notification_id: int, session: Session):
    notification = session.exec(select(Notification).where(Notification.id == notification_id)).one_or_none()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(notification)
    session.commit()
    return {"message": "Notification Deleted Successfully"}

# Update Notification by ID
def update_notification_by_id(notification_id: int, to_update_notification_data: NotificationUpdate, session: Session):
    notification = session.exec(select(Notification).where(Notification.id == notification_id)).one_or_none()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification_data = to_update_notification_data.model_dump(exclude_unset=True)
    notification.sqlmodel_update(notification_data)
    session.add(notification)
    session.commit()
    return notification
    