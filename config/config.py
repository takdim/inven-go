import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL Database Configuration
    # IMPORTANT: Set these values in .env file for production!
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'your_password_here'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'inventaris_gudang'
    
    # URL encode password untuk menghindari karakter special
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Set False di production
