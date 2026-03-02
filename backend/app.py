# app.py
# Aplicación principal Flask - SEGURA (OWASP Top 10:2025)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from registro import registro_bp
from login import login_bp
from coches import coches_bp
from config import (
    DEBUG_MODE,
    ALLOWED_ORIGINS,
    SECURITY_HEADERS,
    RATE_LIMIT_API
)
from datetime import datetime
import os

# ============================================
# CREAR APLICACIÓN FLASK
# ============================================

app = Flask(__name__)

# ============================================
# CONFIGURACIÓN DE SEGURIDAD (A02)
# ============================================

# Debug mode controlado por variable de entorno
app.config['DEBUG'] = DEBUG_MODE
app.config['ENV'] = 'development' if DEBUG_MODE else 'production'

# Ocultar información del servidor
app.config['SERVER_NAME'] = None

# ============================================
# CORS CONFIGURADO CORRECTAMENTE (A02)
# ============================================

CORS(app, 
     origins=ALLOWED_ORIGINS,  # Solo orígenes permitidos
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# ============================================
# RATE LIMITING (A06, A07)
# ============================================

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[RATE_LIMIT_API],
    storage_uri="memory://",  # En producción usar Redis
)

# ============================================
# HEADERS DE SEGURIDAD (A02)
# ============================================

@app.after_request
def add_security_headers(response):
    """
    Añade headers de seguridad a todas las respuestas
    Protege contra: XSS, Clickjacking, MIME sniffing, etc.
    """
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    
    # Ocultar información del servidor
    response.headers['Server'] = 'AppCoches'
    
    return response

# ============================================
# REGISTRAR BLUEPRINTS
# ============================================

app.register_blueprint(registro_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(coches_bp, url_prefix='/api')

# ============================================
# RUTAS PRINCIPALES
# ============================================

@app.route('/')
@limiter.limit("10 per minute")
def inicio():
    """Ruta de inicio con información de la API"""
    return jsonify({
        'application': 'AppCoches API',
        'version': '2.0.0',
        'status': 'running',
        'security': 'OWASP Top 10:2025 Protected',
        'endpoints': {
            'authentication': {
                'registro': 'POST /api/registro',
                'login': 'POST /api/login',
                'verificar_token': 'GET /api/verificar-token'
            },
            'coches': {
                'listar': 'GET /api/coches',
                'obtener': 'GET /api/coches/<id>',
                'crear': 'POST /api/coches (admin)',
                'editar': 'PUT /api/coches/<id> (admin)',
                'eliminar': 'DELETE /api/coches/<id> (admin)',
                'marcas': 'GET /api/marcas',
                'estadisticas': 'GET /api/estadisticas',
                'imagenes': 'GET /api/uploads/<filename>'
            }
        },
        'security_features': [
            'JWT Authentication',
            'Role-Based Access Control',
            'Rate Limiting',
            'Account Lockout Protection',
            'bcrypt Password Hashing',
            'Security Headers',
            'CORS Protection',
            'Input Validation',
            'SQL Injection Protection'
        ]
    })

@app.route('/health')
@limiter.limit("20 per minute")
def health_check():
    """Health check endpoint para monitoreo"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================
# MANEJO DE ERRORES (A10)
# ============================================

@app.errorhandler(400)
def bad_request(error):
    """Manejo de peticiones incorrectas"""
    return jsonify({
        'success': False,
        'error': 'Bad Request',
        'message': 'La petición contiene datos inválidos'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    """Manejo de acceso no autorizado"""
    return jsonify({
        'success': False,
        'error': 'Unauthorized',
        'message': 'Autenticación requerida'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    """Manejo de acceso prohibido"""
    return jsonify({
        'success': False,
        'error': 'Forbidden',
        'message': 'No tienes permisos para acceder a este recurso'
    }), 403

@app.errorhandler(404)
def not_found(error):
    """Manejo de recursos no encontrados"""
    return jsonify({
        'success': False,
        'error': 'Not Found',
        'message': 'El recurso solicitado no existe'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejo de métodos no permitidos"""
    return jsonify({
        'success': False,
        'error': 'Method Not Allowed',
        'message': 'El método HTTP no está permitido para este endpoint'
    }), 405

@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Manejo de exceso de rate limit"""
    return jsonify({
        'success': False,
        'error': 'Too Many Requests',
        'message': 'Has excedido el límite de peticiones. Intenta más tarde'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos del servidor"""
    print(f"Internal Server Error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'Ha ocurrido un error interno. Por favor, contacta al administrador'
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Manejo genérico de excepciones no capturadas"""
    print(f"Unhandled Exception: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'Ha ocurrido un error inesperado'
    }), 500

# ============================================
# CREAR DIRECTORIOS NECESARIOS
# ============================================

def crear_directorios():
    """Crea directorios necesarios si no existen"""
    directories = ['uploads/coches']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directorio creado: {directory}")

# ============================================
# EJECUTAR APLICACIÓN
# ============================================

if __name__ == '__main__':
    # Crear directorios
    crear_directorios()
    
    # Log de inicio
    print("=" * 50)
    print("Servidor Flask iniciado")
    print(f"Modo: {'Desarrollo' if DEBUG_MODE else 'Producción'}")
    print(f"Rate Limiting: Activado")
    print(f"Security Headers: Activados")
    print(f"CORS: Configurado para {ALLOWED_ORIGINS}")
    print("API disponible en: http://localhost:5000")
    print("=" * 50)
    
    # Ejecutar servidor
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )