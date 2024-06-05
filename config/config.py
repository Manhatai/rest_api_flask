from dotenv import load_dotenv
import os

load_dotenv()

class Config: # We need to create a Config class for our config to become modular (.config.from_object())
    def __str2bool(value):
        return value.lower() in ("true", "1")

    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/postgres'
    SECRET_KEY = os.getenv("SECRET_KEY")
    IS_DEBUG = __str2bool(os.getenv("IS_DEBUG"))
