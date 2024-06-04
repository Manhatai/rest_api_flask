from dotenv import load_dotenv
import os

load_dotenv()

class Config: # We need to create a Config class for our config to become modular (.config.from_object())
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/postgres'
    SECRET_KEY = os.getenv("SECRET_KEY")
