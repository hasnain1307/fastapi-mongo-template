from config.urls import urls
from .create_database import MongoDBClient
from .base_model import BaseMongoModel, CreateSchemaType
from .models import TenantModel

# Create an asynchronous MongoClient
db_client = MongoDBClient(urls.mongo_database_conn_str)
mongo_client = db_client.db_client
bot_config_db = db_client.db_name
