from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str = Field(..., env="DATABASE_HOST")
    database_db: str = Field(..., env="DATABASE_DB")
    database_name: str = Field("mongoadmin", env="DATABASE_USER")
    database_password: str = Field("secret", env="DATABASE_PASSWORD")
    database_port: int = Field(27017, env="DATABASE_PORT")

    @property
    def _database_url(self):
        return f"{self.database_host}:{self.database_port}"

    @property
    def mongo_database_conn_str(self) -> str:
        return f"mongodb://{self.database_name}:{self.database_password}@{self._database_url}/{self.database_db}?authSource=admin"


urls = Settings()

print(urls.mongo_database_conn_str,flush=True)
