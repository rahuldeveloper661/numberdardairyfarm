from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["mydatabase"]
collection = db["users"]

# ObjectId converter


def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }


@app.post("/users/")
async def create_user(user: dict):
    result = await collection.insert_one(user)
    new_user = await collection.find_one({"_id": result.inserted_id})
    return user_serializer(new_user)


@app.get("/users/")
async def get_users():
    users = []
    async for user in collection.find():
        users.append(user_serializer(user))
    return users
