import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from db import client
from typing import Optional
from datetime import datetime
from bson import ObjectId

app = FastAPI()

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

db = client.get_database(DB_NAME)
collection = db["mood"]

class Mood(BaseModel):
    user_id: str
    mood: int
    timestamp: datetime
    note: Optional[str] = None

class MoodUpdate(BaseModel):
    mood: Optional[int] = None
    timestamp: Optional[datetime] = None
    note: Optional[str] = None

# Helper to convert MongoDB document to dict with string id
def mood_helper(mood_doc):
    return {
        "id": str(mood_doc["_id"]),
        "user_id": mood_doc["user_id"],
        "mood": mood_doc["mood"],
        "timestamp": mood_doc["timestamp"],
        "note": mood_doc.get("note")
    }

@app.post("/mood", response_model=dict)
async def create_mood(mood: Mood):
    try:
        result = collection.insert_one(mood.dict())
        new_mood = collection.find_one({"_id": result.inserted_id})
        return mood_helper(new_mood)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mood", response_model=list)
async def get_moods(user_id: Optional[str] = None):
    query = {"user_id": user_id} if user_id else {}
    moods = [mood_helper(m) for m in collection.find(query)]
    return moods

@app.patch("/mood/{mood_id}", response_model=dict)
async def update_mood(mood_id: str, mood_update: MoodUpdate):
    update_data = {k: v for k, v in mood_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = collection.update_one({"_id": ObjectId(mood_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Mood not found.")
    updated_mood = collection.find_one({"_id": ObjectId(mood_id)})
    return mood_helper(updated_mood)

@app.delete("/mood/{mood_id}")
async def delete_mood(mood_id: str):
    result = collection.delete_one({"_id": ObjectId(mood_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mood not found.")
    return {"detail": "Mood deleted successfully."}

