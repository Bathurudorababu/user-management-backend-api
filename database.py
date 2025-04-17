from pymongo.mongo_client import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv()

MONGO_URI= os.getenv("MONGODB_URL")

client = MongoClient(MONGO_URI)

db = client["user_management"]

user_collection = db["users"]
token_collection = db["tokens"]


# from pymongo import MongoClient
# from pymongo.errors import ServerSelectionTimeoutError

# # MongoDB URI (replace with your actual URI)
# mongo_uri = "mongodb://admin:secret@localhost:27017"

# try:
#     # Try to establish a connection
#     client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
#     # Check if the connection is successful
#     client.admin.command('ping')
#     print("MongoDB connection successful!")
# except ServerSelectionTimeoutError as e:
#     print("Error connecting to MongoDB:", e)
