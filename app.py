from fastapi import FastAPI

from configs.database import Base, engine
from routers.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)