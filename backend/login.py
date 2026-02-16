# login.py
# Gestión del inicio de sesión

from flask import Blueprint, request, jsonify
from database import execute_query
import hashlib
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

login_bp = Blueprint('login', __name__)

def hash_password(password):
    """Encripta la contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generar_token(user_id, email, rol):
    """Genera un token JWT para el usuario"""
    payload = {
        'user_id': user_id,
        'email': email,
        'rol': rol,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token válido por 24 horas
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@login_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    """
    Endpoint para iniciar sesión
    Espera: email, password
    Retorna: token JWT
    """
    try:
        data = request.get_json()
        
        # Validar datos
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email y contraseña son obligatorios'
            }), 400
        
        # Encriptar contraseña para comparar
        password_hash = hash_password(password)
        
        # Buscar usuario
        query = """
            SELECT id, nombre, email, rol 
            FROM usuarios 
            WHERE email = %s AND password = %s
        """
        resultado = execute_query(query, (email, password_hash), fetch=True)
        
        if not resultado:
            return jsonify({
                'success': False,
                'message': 'Email o contraseña incorrectos'
            }), 401
        
        usuario = resultado[0]
        
        # Generar token JWT
        token = generar_token(usuario['id'], usuario['email'], usuario['rol'])
        
        return jsonify({
            'success': True,
            'message': 'Inicio de sesión exitoso',
            'token': token,
            'usuario': {
                'id': usuario['id'],
                'nombre': usuario['nombre'],
                'email': usuario['email'],
                'rol': usuario['rol']
            }
        }), 200
    
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@login_bp.route('/verificar-token', methods=['GET'])
def verificar_token():
    """Verifica si un token JWT es válido"""
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        # Remover "Bearer " si existe
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        return jsonify({
            'success': True,
            'usuario': {
                'id': payload['user_id'],
                'email': payload['email'],
                'rol': payload['rol']
            }
        }), 200
    
    except jwt.ExpiredSignatureError:
        return jsonify({
            'success': False,
            'message': 'Token expirado'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'success': False,
            'message': 'Token inválido'
        }), 401
    except Exception as e:
        print(f"Error al verificar token: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
