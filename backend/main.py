from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.LoginAPI import login_router
from api.UserAPI import user_router
from database import config_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute before app start
    config_db.wait_for_database()
    config_db.create_db()

    yield

    # Execute after app end
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(login_router)