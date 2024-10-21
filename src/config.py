from base64 import b64decode
from functools import lru_cache
from typing import Any, Dict, Optional, ClassVar
import sqlalchemy.dialects.postgresql

from pydantic import Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: ClassVar[str] = 'mysql+pymysql://test:Paccy%40123456789@localhost:3306/yokai'

    
# from base64 import b64decode
# from functools import lru_cache
# from typing import Any, Dict, Optional
# from pydantic import BaseSettings
# from dotenv import load_dotenv
# from sqlalchemy import create_engine

# load_dotenv()

# @lru_cache()
# def get_settings():
#     return Settings()

# class Settings(BaseSettings):
#     HOST: str = Field(..., env='PGDB_HOST')
#     USER: str = Field(..., env='PGDB_USER')
#     PASSWORD: str = Field(..., env='PGDB_PASSWORD')
#     DB: str = Field(..., env='PGDB_DB')
#     PORT: int = Field(..., env='PGDB_PORT')

# def get_database_url() -> str:
#     settings = get_settings()
#     return f"mysql+mysqlconnector://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}"

# def get_engine():
#     database_url = get_database_url()
#     return create_engine(database_url)

# # Example usage:
# if __name__ == "__main__":
#     engine = get_engine()
#     # Test the connection
#     try:
#         with engine.connect() as connection:
#             print("Connection successful")
#     except Exception as e:
#         print(f"Connection failed: {e}")
    
