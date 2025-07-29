from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PollCreate(BaseModel):
    question: str


class PollOut(BaseModel):
    id: int
    question: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
