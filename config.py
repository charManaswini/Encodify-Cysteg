import os

class Config:
    SECRET_KEY = os.urandom(24)  # For session encryption
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:manu123@localhost/encodify_db'  # PostgreSQL URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)  # You can keep it as this, which should be secure
