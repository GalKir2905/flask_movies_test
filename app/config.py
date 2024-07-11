import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', "sqlite:///:memory:")
    SECRET_KEY = os.getenv('SECRET_KEY', 'YOUR_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
