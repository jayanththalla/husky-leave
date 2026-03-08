from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import get_settings
from datetime import datetime

settings = get_settings()
client = None
db = None

def connect_to_mongo():
    global client, db
    try:
        client = MongoClient(settings.mongodb_uri)
        db = client.leave_management
        client.admin.command('ping')
        print("Successfully connected to MongoDB")
        
        # Create indexes
        create_indexes()
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

def close_mongo_connection():
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed")

def create_indexes():
    """Create necessary indexes for efficient queries"""
    if db is not None:
        # Users collection
        db.users.create_index("email", unique=True)
        db.users.create_index("employee_id", unique=True, sparse=True)
        
        # Leave requests collection
        db.leave_requests.create_index("employee_id")
        db.leave_requests.create_index("created_at")
        db.leave_requests.create_index([("employee_id", 1), ("status", 1)])

def get_database():
    return db
