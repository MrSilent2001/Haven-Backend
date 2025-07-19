import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from util.db import client
from routes.mood import router as mood_router
from routes.user import router as user_router
from routes.meditation import router as meditation_router
from routes.ncsmusic import router as ncsmusic_router

app = FastAPI()

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

db = client.get_database(DB_NAME)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pass db to routers if needed (or set up in each module)
app.include_router(mood_router, prefix="/mood")
app.include_router(user_router, prefix="/user")
app.include_router(meditation_router, prefix="/meditation")
app.include_router(ncsmusic_router, prefix="/ncsmusic")