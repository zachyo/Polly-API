from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, auth
from .database import get_db

router = APIRouter()


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/polls", response_model=List[schemas.PollOut])
def get_polls(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    polls = db.query(models.Poll).offset(skip).limit(limit).all()
    return polls


@router.post("/polls", response_model=schemas.PollOut)
def create_poll(
    poll: schemas.PollCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_poll = models.Poll(question=poll.question, owner_id=current_user.id)
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)
    return new_poll


@router.delete("/polls/{poll_id}", status_code=204)
def delete_poll(
    poll_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    poll = (
        db.query(models.Poll)
        .filter(models.Poll.id == poll_id, models.Poll.owner_id == current_user.id)
        .first()
    )
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found or not authorized")
    db.delete(poll)
    db.commit()
    return None
