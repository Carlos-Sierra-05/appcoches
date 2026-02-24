# registro.py
# Gestión del registro de usuarios (OWASP A04, A07, A09)

from flask import Blueprint, request, jsonify
from database import execute_query
import bcrypt
import re
from security_logger import (
    log_register_success, 
    log_register_failure,
    get_client_ip,
    get_user_agent
)

registro_bp = Blueprint('registro', __name__)

# ============================================
# VALIDACIÓN DE CONTRASEÑAS (A07)
# ============================================

def validar_contraseña(password):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    # Opcional: verificar caracteres especiales
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, "Contraseña válida"

def validar_email(email):
    """
    Valida formato de email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ============================================
# ENDPOINT DE REGISTRO
# ============================================

@registro_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    """
    Endpoint para registrar un nuevo usuario
    Protegido contra: A04 (Crypto), A07 (Auth), A09 (Logging)
    """
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        data = request.get_json()
        
        # Validar datos
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()  # Email en minúsculas
        password = data.get('password', '')
        
        # ============================================
        # VALIDACIONES DE ENTRADA (A07)
        # ============================================
        
        if not nombre or not email or not password:
            log_register_failure(email, ip_address, 'Campos vacíos')
            return jsonify({
                'success': False,
                'message': 'Todos los campos son obligatorios'
            }), 400
        
        # Validar longitud del nombre
        if len(nombre) < 2 or len(nombre) > 100:
            log_register_failure(email, ip_address, 'Nombre inválido')
            return jsonify({
                'success': False,
                'message': 'El nombre debe tener entre 2 y 100 caracteres'
            }), 400
        
        # Validar formato de email
        if not validar_email(email):
            log_register_failure(email, ip_address, 'Email inválido')
            return jsonify({
                'success': False,
                'message': 'Formato de email inválido'
            }), 400
        
        # Validar contraseña
        password_valida, mensaje = validar_contraseña(password)
        if not password_valida:
            log_register_failure(email, ip_address, mensaje)
            return jsonify({
                'success': False,
                'message': mensaje
            }), 400
        
        # ============================================
        # VERIFICAR SI EL EMAIL YA EXISTE
        # ============================================
        
        query_check = "SELECT id FROM usuarios WHERE email = %s"
        resultado = execute_query(query_check, (email,), fetch=True)
        
        if resultado:
            log_register_failure(email, ip_address, 'Email ya registrado')
            return jsonify({
                'success': False,
                'message': 'El email ya está registrado'
            }), 400
        
        # ============================================
        # ENCRIPTAR CONTRASEÑA CON BCRYPT (A04)
        # ============================================
        
        # Generar salt y hashear contraseña
        salt = bcrypt.gensalt(rounds=12)  # 12 rondas (seguro y rápido)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # ============================================
        # INSERTAR USUARIO
        # ============================================
        
        query_insert = """
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (%s, %s, %s, 'usuario')
        """
        result = execute_query(
            query_insert, 
            (nombre, email, password_hash.decode('utf-8'))
        )
        
        if result and result['affected_rows'] > 0:
            # Log de éxito (A09)
            log_register_success(email, ip_address)
            
            return jsonify({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'user_id': result['last_id']
            }), 201
        else:
            log_register_failure(email, ip_address, 'Error en base de datos')
            return jsonify({
                'success': False,
                'message': 'Error al registrar usuario'
            }), 500
    
    except Exception as e:
        # Log de error (A09, A10)
        log_register_failure(
            email if 'email' in locals() else 'unknown',
            ip_address,
            f'Exception: {str(e)}'
        )
        print(f"Error en registro: {e}")
        
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500