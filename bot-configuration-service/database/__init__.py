import motor.motor_asyncio
from config.urls import urls

# # Your MongoDB models
# from .models import Users, Bots, Tenants

# Create an asynchronous MongoClient
db_client = motor.motor_asyncio.AsyncIOMotorClient(urls.mongo_database_conn_str)

# Select your database
db_object = db_client["bot_configuration"]  # Replace with your database name

# Initialize asynchronous collections
users_collection = db_object["users"]
bots_collection = db_object["bots"]
tenants_collection = db_object["tenants"]