from pydantic import BaseModel, ConfigDict
from datetime import datetime, UTC
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(from_attributes=True)
