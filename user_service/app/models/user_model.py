from sqlmodel import SQLModel,Field
from typing import Optional,Annotated
from pydantic import BaseModel
from fastapi import Form
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"




class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    role: Role = Field(default=Role.USER)
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    # role: Optional[Role] = None


class Register_User (BaseModel):
            username: Annotated[
            str,
            Form(),
        ]
            email: Annotated[
            str,
            Form(),
        ]
            password: Annotated[
            str,
            Form(),
        ]


class Token (BaseModel):
        access_token:str
        token_type: str

class TokenData (BaseModel):
        username:str