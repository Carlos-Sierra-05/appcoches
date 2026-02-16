# registro.py
# Gestión del registro de usuarios

from flask import Blueprint, request, jsonify
from database import execute_query
import hashlib

registro_bp = Blueprint('registro', __name__)

def hash_password(password):
    """Encripta la contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@registro_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    """
    Endpoint para registrar un nuevo usuario
    Espera: nombre, email, password
    """
    try:
        data = request.get_json()
        
        # Validar datos
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not nombre or not email or not password:
            return jsonify({
                'success': False,
                'message': 'Todos los campos son obligatorios'
            }), 400
        
        # Validar formato de email básico
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': 'Email inválido'
            }), 400
        
        # Validar longitud de contraseña
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'La contraseña debe tener al menos 6 caracteres'
            }), 400
        
        # Verificar si el email ya existe
        query_check = "SELECT id FROM usuarios WHERE email = %s"
        resultado = execute_query(query_check, (email,), fetch=True)
        
        if resultado:
            return jsonify({
                'success': False,
                'message': 'El email ya está registrado'
            }), 400
        
        # Encriptar contraseña
        password_hash = hash_password(password)
        
        # Insertar usuario
        query_insert = """
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (%s, %s, %s, 'usuario')
        """
        result = execute_query(query_insert, (nombre, email, password_hash))
        
        if result and result['affected_rows'] > 0:
            return jsonify({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'user_id': result['last_id']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Error al registrar usuario'
            }), 500
    
    except Exception as e:
        print(f"Error en registro: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
