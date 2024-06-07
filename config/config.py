from dotenv import load_dotenv
import os

load_dotenv()

class Config: # We need to create a Config class for our config to become modular (.config.from_object())
    def __str2bool(value):
        return value.lower() in ("true", "1")
    __DB_BASE_HOST = f"{os.getenv("REST_API_DB_HOST")}:{os.getenv("REST_API_DB_PORT")}"
    __DB_CREDENTIALS = f"{os.getenv("REST_API_DB_LOGIN")}:{os.getenv("REST_API_DB_PASSWORD")}"
    SQLALCHEMY_DATABASE_URI = f'postgresql://{__DB_CREDENTIALS}@{__DB_BASE_HOST}/{os.getenv("REST_API_DB_NAME")}'
    SECRET_KEY = os.getenv("REST_API_SECRET_KEY")
    IS_DEBUG = __str2bool(os.getenv("REST_API_IS_DEBUG"))
    REST_API_ENV_NAME = os.getenv("REST_API_ENV_NAME")