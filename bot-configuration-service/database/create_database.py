import motor.motor_asyncio


class MongoDBClient:
    def __init__(self, conn_str):
        self.db_client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)
        self.db_name = self.db_client.get_database("bot_configuration")
