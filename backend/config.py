# config.py
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'AppCoches9393'),
    'database': os.getenv('DB_NAME', 'appcoches'),
    'charset': 'utf8mb4'
}

SECRET_KEY = 'tu_clave_secreta_super_segura_123'