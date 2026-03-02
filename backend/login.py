# login.py
# Gestión del inicio de sesión (OWASP A04, A07)

from flask import Blueprint, request, jsonify
from database import execute_query
import bcrypt
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY
import time

login_bp = Blueprint('login', __name__)

# ============================================
# CONTROL DE INTENTOS FALLIDOS (A07)
# ============================================

# Diccionario para rastrear intentos fallidos
# En producción, usar Redis o base de datos
failed_attempts = {}
locked_accounts = {}

MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutos en segundos

def check_account_locked(email):
    """Verifica si una cuenta está bloqueada"""
    if email in locked_accounts:
        lock_time = locked_accounts[email]
        if time.time() - lock_time < LOCKOUT_DURATION:
            return True, int(LOCKOUT_DURATION - (time.time() - lock_time))
        else:
            # Desbloquear cuenta
            del locked_accounts[email]
            if email in failed_attempts:
                del failed_attempts[email]
            return False, 0
    return False, 0

def register_failed_attempt(email):
    """Registra un intento fallido"""
    if email not in failed_attempts:
        failed_attempts[email] = {'count': 0, 'last_attempt': time.time()}
    
    failed_attempts[email]['count'] += 1
    failed_attempts[email]['last_attempt'] = time.time()
    
    # Si excede el límite, bloquear cuenta
    if failed_attempts[email]['count'] >= MAX_ATTEMPTS:
        locked_accounts[email] = time.time()
        print(f"ACCOUNT_LOCKED | Email: {email} | Reason: Too many failed attempts")
        return True
    
    return False

def clear_failed_attempts(email):
    """Limpia intentos fallidos después de login exitoso"""
    if email in failed_attempts:
        del failed_attempts[email]
    if email in locked_accounts:
        del locked_accounts[email]

# ============================================
# GENERACIÓN DE TOKEN JWT (A04)
# ============================================

def generar_token(user_id, email, rol):
    """
    Genera un token JWT para el usuario
    Duración reducida: 2 horas (antes 24h)
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'rol': rol,
        'iat': datetime.utcnow(),  # Issued at
        'exp': datetime.utcnow() + timedelta(hours=2)  # Expira en 2 horas
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# ============================================
# ENDPOINT DE LOGIN
# ============================================

@login_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    """
    Endpoint para iniciar sesión
    Protegido contra: A04 (Crypto), A07 (Auth)
    """
    try:
        data = request.get_json()
        
        # Validar datos
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            print(f"LOGIN_FAILURE | Email: {email} | Reason: Campos vacíos")
            return jsonify({
                'success': False,
                'message': 'Email y contraseña son obligatorios'
            }), 400
        
        # ============================================
        # VERIFICAR SI LA CUENTA ESTÁ BLOQUEADA (A07)
        # ============================================
        
        is_locked, remaining_time = check_account_locked(email)
        if is_locked:
            print(f"LOGIN_FAILURE | Email: {email} | Reason: Cuenta bloqueada")
            return jsonify({
                'success': False,
                'message': f'Cuenta bloqueada temporalmente. Intenta de nuevo en {remaining_time // 60} minutos'
            }), 429  # Too Many Requests
        
        # ============================================
        # BUSCAR USUARIO
        # ============================================
        
        query = """
            SELECT id, nombre, email, password, rol 
            FROM usuarios 
            WHERE email = %s
        """
        resultado = execute_query(query, (email,), fetch=True)
        
        if not resultado:
            # Usuario no existe
            print(f"LOGIN_FAILURE | Email: {email} | Reason: Usuario no existe")
            register_failed_attempt(email)
            return jsonify({
                'success': False,
                'message': 'Email o contraseña incorrectos'
            }), 401
        
        usuario = resultado[0]
        
        # ============================================
        # VERIFICAR CONTRASEÑA CON BCRYPT (A04)
        # ============================================
        
        password_hash_db = usuario['password']
        
        # Verificar si la contraseña es bcrypt o SHA-256 (para migración)
        if password_hash_db.startswith('$2'):
            # Es bcrypt
            password_correcta = bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash_db.encode('utf-8')
            )
        else:
            # Es SHA-256 antiguo (para compatibilidad temporal)
            import hashlib
            password_hash_input = hashlib.sha256(password.encode()).hexdigest()
            password_correcta = (password_hash_db == password_hash_input)
            
            # Si es correcta, actualizar a bcrypt
            if password_correcta:
                salt = bcrypt.gensalt(rounds=12)
                new_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                execute_query(
                    "UPDATE usuarios SET password = %s WHERE id = %s",
                    (new_hash.decode('utf-8'), usuario['id'])
                )
        
        if not password_correcta:
            # Contraseña incorrecta
            print(f"LOGIN_FAILURE | Email: {email} | Reason: Contraseña incorrecta")
            is_locked = register_failed_attempt(email)
            
            if is_locked:
                return jsonify({
                    'success': False,
                    'message': 'Demasiados intentos fallidos. Cuenta bloqueada temporalmente'
                }), 429
            
            remaining_attempts = MAX_ATTEMPTS - failed_attempts.get(email, {}).get('count', 0)
            return jsonify({
                'success': False,
                'message': f'Email o contraseña incorrectos. Te quedan {remaining_attempts} intentos'
            }), 401
        
        # ============================================
        # LOGIN EXITOSO
        # ============================================
        
        # Limpiar intentos fallidos
        clear_failed_attempts(email)
        
        # Generar token JWT
        token = generar_token(usuario['id'], usuario['email'], usuario['rol'])
        
        print(f"LOGIN_SUCCESS | Email: {email}")
        
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
        print(f"ERROR en login: {e}")
        
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

# ============================================
# VERIFICACIÓN DE TOKEN
# ============================================

@login_bp.route('/verificar-token', methods=['GET'])
def verificar_token():
    """
    Verifica si un token JWT es válido
    """
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            print("UNAUTHORIZED_ACCESS | /verificar-token | Reason: Token no proporcionado")
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        # Remover "Bearer " si existe
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verificar token
        try:
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
            print(f"TOKEN_EXPIRED | Email: {payload.get('email', 'unknown')}")
            return jsonify({
                'success': False,
                'message': 'Token expirado. Por favor, inicia sesión nuevamente'
            }), 401
        
        except jwt.InvalidTokenError:
            print("INVALID_TOKEN")
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