import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_pizzeria_123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Configuración de conexión a MySQL.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1605@localhost/pizzeria_db'