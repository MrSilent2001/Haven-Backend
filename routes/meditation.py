from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from bson import ObjectId
from util.db import client
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
db = client.get_database(DB_NAME)
collection = db["meditation"]

router = APIRouter()

class Meditation(BaseModel):
    user_id: str
    timestamp: datetime
    duration: timedelta
    comment: Optional[str] = None

class MeditationUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    duration: Optional[timedelta] = None
    comment: Optional[str] = None

def meditation_helper(meditation_doc):
    return {
        "id": str(meditation_doc["_id"]),
        "user_id": meditation_doc["user_id"],
        "timestamp": meditation_doc["timestamp"],
        "duration": meditation_doc["duration"],
        "comment": meditation_doc.get("comment")
    }

@router.post("/", response_model=dict)
async def create_meditation(meditation: Meditation):
    try:
        doc = meditation.dict()
        # Store duration as total seconds for BSON compatibility
        doc["duration"] = doc["duration"].total_seconds()
        result = collection.insert_one(doc)
        new_meditation = collection.find_one({"_id": result.inserted_id})
        # Convert duration back to timedelta for response
        new_meditation["duration"] = timedelta(seconds=new_meditation["duration"])
        return meditation_helper(new_meditation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list)
async def get_meditations(user_id: Optional[str] = None):
    query = {"user_id": user_id} if user_id else {}
    meditations = []
    for m in collection.find(query):
        m["duration"] = timedelta(seconds=m["duration"])
        meditations.append(meditation_helper(m))
    return meditations

@router.patch("/{meditation_id}", response_model=dict)
async def update_meditation(meditation_id: str, meditation_update: MeditationUpdate):
    update_data = {k: v for k, v in meditation_update.dict().items() if v is not None}
    if "duration" in update_data:
        update_data["duration"] = update_data["duration"].total_seconds()
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = collection.update_one({"_id": ObjectId(meditation_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Meditation not found.")
    updated_meditation = collection.find_one({"_id": ObjectId(meditation_id)})
    updated_meditation["duration"] = timedelta(seconds=updated_meditation["duration"])
    return meditation_helper(updated_meditation)

@router.delete("/{meditation_id}")
async def delete_meditation(meditation_id: str):
    result = collection.delete_one({"_id": ObjectId(meditation_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Meditation not found.")
    return {"detail": "Meditation deleted successfully."}
