# security_logger.py
# Sistema de logging de seguridad (OWASP A09)
# Optimizado para Docker con volúmenes persistentes

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import sys

# ============================================
# CONFIGURACIÓN DEL LOGGER PARA DOCKER
# ============================================

def setup_security_logger():
    """
    Configura el sistema de logging de seguridad
    Compatible con Docker: logs a archivo Y consola
    """
    # Directorio de logs (persistente en Docker mediante volumen)
    log_dir = os.getenv('LOG_DIR', '/app/logs')
    
    # Crear directorio de logs si no existe
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"✓ Directorio de logs creado: {log_dir}")
    except Exception as e:
        print(f"⚠ No se pudo crear directorio de logs: {e}")
        log_dir = '/tmp'  # Fallback a /tmp
    
    # Configurar logger principal
    logger = logging.getLogger('security')
    logger.setLevel(logging.INFO)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # ============================================
    # HANDLER 1: ARCHIVO (persistente via volumen)
    # ============================================
    try:
        log_file = os.path.join(log_dir, 'security.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        print(f"✓ Logger de archivo configurado: {log_file}")
    except Exception as e:
        print(f"⚠ No se pudo configurar logger de archivo: {e}")
    
    # ============================================
    # HANDLER 2: CONSOLA (para docker logs)
    # ============================================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Cambiado a INFO para ver todo
    
    # Formato con colores para consola (opcional)
    console_formatter = logging.Formatter(
        '🔒 %(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Log de inicio
    logger.info("=" * 60)
    logger.info("SISTEMA DE LOGGING DE SEGURIDAD INICIADO")
    logger.info(f"Logs de archivo: {log_dir}/security.log")
    logger.info(f"Logs de consola: Activos (ver con docker-compose logs)")
    logger.info("=" * 60)
    
    return logger

# Logger global
security_logger = setup_security_logger()

# ============================================
# FUNCIONES DE LOGGING
# ============================================

def log_login_success(email, ip_address, user_agent):
    """Registra inicio de sesión exitoso"""
    security_logger.info(f"LOGIN_SUCCESS | Email: {email} | IP: {ip_address} | UserAgent: {user_agent[:50]}")

def log_login_failure(email, ip_address, reason, user_agent):
    """Registra intento de inicio de sesión fallido"""
    security_logger.warning(f"LOGIN_FAILURE | Email: {email} | IP: {ip_address} | Reason: {reason} | UserAgent: {user_agent[:50]}")

def log_account_locked(email, ip_address):
    """Registra bloqueo de cuenta por intentos fallidos"""
    security_logger.warning(f"ACCOUNT_LOCKED | Email: {email} | IP: {ip_address} | Reason: Too many failed attempts")

def log_register_success(email, ip_address):
    """Registra registro exitoso"""
    security_logger.info(f"REGISTER_SUCCESS | Email: {email} | IP: {ip_address}")

def log_register_failure(email, ip_address, reason):
    """Registra intento de registro fallido"""
    security_logger.warning(f"REGISTER_FAILURE | Email: {email} | IP: {ip_address} | Reason: {reason}")

def log_unauthorized_access(endpoint, ip_address, reason):
    """Registra intento de acceso no autorizado"""
    security_logger.warning(f"UNAUTHORIZED_ACCESS | Endpoint: {endpoint} | IP: {ip_address} | Reason: {reason}")

def log_admin_action(action, admin_email, resource_id, ip_address):
    """Registra acciones de administrador"""
    security_logger.info(f"ADMIN_ACTION | Action: {action} | Admin: {admin_email} | Resource: {resource_id} | IP: {ip_address}")

def log_token_expired(email, ip_address):
    """Registra intento de uso de token expirado"""
    security_logger.warning(f"TOKEN_EXPIRED | Email: {email} | IP: {ip_address}")

def log_invalid_token(ip_address):
    """Registra intento de uso de token inválido"""
    security_logger.warning(f"INVALID_TOKEN | IP: {ip_address}")

def log_rate_limit_exceeded(endpoint, ip_address):
    """Registra exceso de rate limit"""
    security_logger.warning(f"RATE_LIMIT_EXCEEDED | Endpoint: {endpoint} | IP: {ip_address}")

def log_file_upload(filename, user_email, ip_address, size):
    """Registra subida de archivo"""
    security_logger.info(f"FILE_UPLOAD | File: {filename} | User: {user_email} | IP: {ip_address} | Size: {size} bytes")

def log_suspicious_activity(activity, details, ip_address):
    """Registra actividad sospechosa"""
    security_logger.error(f"SUSPICIOUS_ACTIVITY | Activity: {activity} | Details: {details} | IP: {ip_address}")

def log_sql_injection_attempt(query, ip_address):
    """Registra intento de SQL injection"""
    security_logger.critical(f"SQL_INJECTION_ATTEMPT | Query: {query} | IP: {ip_address}")

def log_error(error_type, error_message, endpoint, ip_address):
    """Registra error de aplicación"""
    security_logger.error(f"APPLICATION_ERROR | Type: {error_type} | Message: {error_message} | Endpoint: {endpoint} | IP: {ip_address}")

def log_password_change(email, ip_address):
    """Registra cambio de contraseña"""
    security_logger.info(f"PASSWORD_CHANGED | Email: {email} | IP: {ip_address}")

def log_data_export(user_email, data_type, ip_address):
    """Registra exportación de datos"""
    security_logger.info(f"DATA_EXPORT | User: {user_email} | Type: {data_type} | IP: {ip_address}")

# ============================================
# UTILIDADES
# ============================================

def get_client_ip(request):
    """
    Obtiene la IP real del cliente
    Compatible con proxies y Docker
    """
    # Primero intentar con X-Forwarded-For (proxies)
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    
    # Luego X-Real-IP
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP').strip()
    
    # Finalmente remote_addr
    return request.remote_addr or 'unknown'

def get_user_agent(request):
    """Obtiene el User-Agent del cliente"""
    return request.headers.get('User-Agent', 'Unknown')[:100]  # Limitar a 100 chars

# ============================================
# ANÁLISIS DE LOGS (Funcionalidad extra)
# ============================================

def get_failed_login_attempts(email, minutes=15):
    """
    Cuenta intentos de login fallidos en los últimos X minutos
    (Para implementar después con Redis o base de datos)
    """
    # TODO: Implementar con caché o BD
    return 0

def analyze_suspicious_patterns():
    """
    Analiza patrones sospechosos en los logs
    (Para implementar después)
    """
    # TODO: Implementar análisis de patrones
    pass

# ============================================
# FUNCIÓN DE UTILIDAD PARA VER LOGS
# ============================================

def tail_logs(lines=50):
    """
    Muestra las últimas N líneas del log
    Útil para debugging
    """
    log_file = os.path.join(os.getenv('LOG_DIR', '/app/logs'), 'security.log')
    try:
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
    except Exception as e:
        return [f"Error al leer logs: {e}"]
