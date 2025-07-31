from pydantic import BaseModel, ConfigDict
from datetime import datetime, UTC
from typing import Optional, List


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


class OptionBase(BaseModel):
    text: str


class OptionCreate(OptionBase):
    pass


class OptionOut(OptionBase):
    id: int
    poll_id: int
    model_config = ConfigDict(from_attributes=True)


class PollCreate(BaseModel):
    question: str
    options: List[str]


class PollOut(BaseModel):
    id: int
    question: str
    created_at: datetime
    owner_id: int
    options: List[OptionOut] = []
    model_config = ConfigDict(from_attributes=True)


class VoteCreate(BaseModel):
    option_id: int


class VoteOut(BaseModel):
    id: int
    user_id: int
    option_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
