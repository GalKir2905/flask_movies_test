import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_TRACK_MODIFICATIONS = False