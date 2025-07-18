import os
from dotenv import load_dotenv
from fastapi import FastAPI
from util.db import client
from routes.mood import router as mood_router
from routes.user import router as user_router

app = FastAPI()

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

db = client.get_database(DB_NAME)

# Pass db to routers if needed (or set up in each module)
app.include_router(mood_router, prefix="/mood")
app.include_router(user_router, prefix="/user")

