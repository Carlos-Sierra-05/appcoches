# config.py
# Configuración de la base de datos

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Cambia esto por tu usuario de MySQL
    'password': 'AppCoches9393',  # Cambia esto por tu contraseña de MySQL
    'database': 'appcoches',
    'charset': 'utf8mb4'
}

# Clave secreta para JWT (cámbiala en producción)
SECRET_KEY = 'tu_clave_secreta_super_segura_123'
