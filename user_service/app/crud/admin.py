from app.models.user_model import User, Role
from app.auth import hash_password
from app.db_engine import engine
from sqlmodel import Session,select
from app import settings
import os




def create_initial_admin():
    with Session(engine) as session:
        # Check if any admin exists
        existing_admin = session.exec(select(User).where(User.role == Role.ADMIN)).first()
        if not existing_admin:
            admin_username = os.getenv("ADMIN_USERNAME", "arsalan")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "123")
            
            admin_user = User(
                username=admin_username,
                email=admin_email,
                password=hash_password(admin_password),
                role=Role.ADMIN
            )
            session.add(admin_user)
            session.commit()