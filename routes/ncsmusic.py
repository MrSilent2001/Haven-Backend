from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from util.db import client
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
db = client.get_database(DB_NAME)
collection = db["ncsmusic"]

router = APIRouter()

class NCSMusic(BaseModel):
    title: str

def ncsmusic_helper(ncsmusic_doc):
    return {
        "id": str(ncsmusic_doc["_id"]),
        "title": ncsmusic_doc["title"]
    }

@router.post("/", response_model=dict)
async def create_ncsmusic(ncsmusic: NCSMusic):
    try:
        result = collection.insert_one(ncsmusic.dict())
        new_ncsmusic = collection.find_one({"_id": result.inserted_id})
        return ncsmusic_helper(new_ncsmusic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list)
async def get_ncsmusic():
    ncsmusic_list = [ncsmusic_helper(n) for n in collection.find()]
    return ncsmusic_list
