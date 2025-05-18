import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gmmlf')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///packages.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False