from pymongo import MongoClient
import os

# Connect to MongoDB using environment variable or default URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["webhook_db"]
collection = db["events"]