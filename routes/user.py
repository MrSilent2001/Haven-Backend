from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from util.db import client
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
db = client.get_database(DB_NAME)
user_collection = db["user"]

router = APIRouter()

class User(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    age: int
    telephone: str
    city: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    telephone: Optional[str] = None
    city: Optional[str] = None

def user_helper(user_doc):
    return {
        "id": str(user_doc["_id"]),
        "user_id": user_doc["user_id"],
        "first_name": user_doc["first_name"],
        "last_name": user_doc["last_name"],
        "age": user_doc["age"],
        "telephone": user_doc["telephone"],
        "city": user_doc["city"]
    }

@router.post("/", response_model=dict)
async def create_user(user: User):
    try:
        result = user_collection.insert_one(user.dict())
        new_user = user_collection.find_one({"_id": result.inserted_id})
        return user_helper(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list)
async def get_users(user_id: Optional[str] = None):
    query = {"user_id": user_id} if user_id else {}
    users = [user_helper(u) for u in user_collection.find(query)]
    return users

@router.patch("/{user_id}", response_model=dict)
async def update_user(user_id: str, user_update: UserUpdate):
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")
    result = user_collection.update_one({"user_id": user_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    updated_user = user_collection.find_one({"user_id": user_id})
    return user_helper(updated_user)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = user_collection.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"detail": "User deleted successfully."} 