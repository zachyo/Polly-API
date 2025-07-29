from fastapi import FastAPI
from api.database import Base, engine
from api import models
from api.routes import router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
