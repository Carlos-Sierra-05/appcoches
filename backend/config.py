# config.py
# Configuración segura de la aplicación (OWASP A02, A04)

import os
import secrets

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'AppCoches9393'),
    'database': os.getenv('DB_NAME', 'appcoches'),
    'charset': 'utf8mb4'
}

# ============================================
# SEGURIDAD JWT (A04)
# ============================================

# IMPORTANTE: En producción, usar variable de entorno
# Generar con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Duración del token (en horas)
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 2))  # Reducido de 24h a 2h

# ============================================
# CONFIGURACIÓN DE SEGURIDAD (A02)
# ============================================

# Modo de desarrollo/producción
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

# CORS - Solo orígenes permitidos
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:8000,http://localhost:3000').split(',')

# ============================================
# RATE LIMITING (A06, A07)
# ============================================

# Límites de peticiones
RATE_LIMIT_LOGIN = os.getenv('RATE_LIMIT_LOGIN', '5 per minute')  # 5 intentos por minuto
RATE_LIMIT_REGISTER = os.getenv('RATE_LIMIT_REGISTER', '3 per hour')  # 3 registros por hora
RATE_LIMIT_API = os.getenv('RATE_LIMIT_API', '100 per minute')  # 100 peticiones API por minuto

# Límites de intentos fallidos
MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
LOCKOUT_DURATION = int(os.getenv('LOCKOUT_DURATION', 900))  # 15 minutos en segundos

# ============================================
# CONTRASEÑAS (A04, A07)
# ============================================

# Requisitos de contraseña
PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL = False  # Opcional

# ============================================
# SUBIDA DE ARCHIVOS (A08)
# ============================================

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = 'uploads/coches'

# ============================================
# LOGGING (A09)
# ============================================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/appcoches.log')
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# ============================================
# HEADERS DE SEGURIDAD (A02)
# ============================================

SECURITY_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'; img-src 'self' data: http://localhost:5000; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}