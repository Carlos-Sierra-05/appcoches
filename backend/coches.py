# coches.py
# Gestión de coches (listar con filtros) - PROTEGIDO CONTRA OWASP A01:2025

from flask import Blueprint, request, jsonify
from database import execute_query
import jwt
from config import SECRET_KEY
import os
import base64
from werkzeug.utils import secure_filename
from functools import wraps

coches_bp = Blueprint('coches', __name__)

# Configuración de subida de archivos
UPLOAD_FOLDER = 'uploads/coches'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================
# DECORADORES PARA PROTECCIÓN DE ACCESO
# ============================================

def verificar_token(f):
    """
    Decorador que verifica que el usuario tenga un token válido
    Protege contra acceso no autenticado
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticación requerido'
            }), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload.get('user_id')
            request.user_email = payload.get('email')
            request.user_rol = payload.get('rol')
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expirado. Por favor, inicia sesión nuevamente'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token inválido'
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error de autenticación'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def requiere_admin(f):
    """
    Decorador que verifica que el usuario sea administrador
    Protege contra escalada de privilegios
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticación requerido'
            }), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            # Verificar que sea admin
            if payload.get('rol') != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Acceso denegado. Se requieren permisos de administrador'
                }), 403
            
            request.user_id = payload.get('user_id')
            request.user_email = payload.get('email')
            request.user_rol = payload.get('rol')
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expirado. Por favor, inicia sesión nuevamente'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token inválido'
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error de autenticación'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# ============================================
# ENDPOINTS PÚBLICOS (sin autenticación)
# ============================================

@coches_bp.route('/coches', methods=['GET'])
def listar_coches():
    """
    Endpoint PÚBLICO para listar coches con filtros opcionales
    No requiere autenticación - cualquiera puede ver el catálogo
    """
    try:
        # Obtener parámetros de filtro
        marca = request.args.get('marca', '').strip()
        modelo = request.args.get('modelo', '').strip()
        año_min = request.args.get('año_min', type=int)
        año_max = request.args.get('año_max', type=int)
        precio_min = request.args.get('precio_min', type=float)
        precio_max = request.args.get('precio_max', type=float)
        ordenar = request.args.get('ordenar', 'id')
        orden = request.args.get('orden', 'ASC').upper()
        
        # Validar orden
        if orden not in ['ASC', 'DESC']:
            orden = 'ASC'
        
        # Validar campo de ordenamiento (prevenir SQL injection)
        campos_validos = ['id', 'marca', 'modelo', 'año', 'precio']
        if ordenar not in campos_validos:
            ordenar = 'id'
        
        # Construir query dinámica
        query = "SELECT * FROM coches WHERE 1=1"
        params = []
        
        # Aplicar filtros
        if marca:
            query += " AND marca LIKE %s"
            params.append(f"%{marca}%")
        
        if modelo:
            query += " AND modelo LIKE %s"
            params.append(f"%{modelo}%")
        
        if año_min:
            query += " AND año >= %s"
            params.append(año_min)
        
        if año_max:
            query += " AND año <= %s"
            params.append(año_max)
        
        if precio_min:
            query += " AND precio >= %s"
            params.append(precio_min)
        
        if precio_max:
            query += " AND precio <= %s"
            params.append(precio_max)
        
        # Añadir ordenamiento
        query += f" ORDER BY {ordenar} {orden}"
        
        # Ejecutar query
        coches = execute_query(query, tuple(params) if params else None, fetch=True)
        
        if coches is None:
            return jsonify({
                'success': False,
                'message': 'Error al obtener coches'
            }), 500
        
        # Formatear precios
        for coche in coches:
            coche['precio'] = float(coche['precio'])
        
        return jsonify({
            'success': True,
            'total': len(coches),
            'coches': coches
        }), 200
    
    except Exception as e:
        print(f"Error al listar coches: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@coches_bp.route('/coches/<int:id>', methods=['GET'])
def obtener_coche(id):
    """
    Endpoint PÚBLICO para obtener un coche específico
    No requiere autenticación
    """
    try:
        # Validar que el ID sea positivo
        if id <= 0:
            return jsonify({
                'success': False,
                'message': 'ID inválido'
            }), 400
        
        query = "SELECT * FROM coches WHERE id = %s"
        resultado = execute_query(query, (id,), fetch=True)
        
        if not resultado:
            return jsonify({
                'success': False,
                'message': 'Coche no encontrado'
            }), 404
        
        coche = resultado[0]
        coche['precio'] = float(coche['precio'])
        
        return jsonify({
            'success': True,
            'coche': coche
        }), 200
    
    except Exception as e:
        print(f"Error al obtener coche: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@coches_bp.route('/marcas', methods=['GET'])
def listar_marcas():
    """
    Endpoint PÚBLICO para obtener lista de marcas
    No requiere autenticación
    """
    try:
        query = "SELECT DISTINCT marca FROM coches ORDER BY marca"
        resultado = execute_query(query, fetch=True)
        
        if resultado is None:
            return jsonify({
                'success': False,
                'message': 'Error al obtener marcas'
            }), 500
        
        marcas = [item['marca'] for item in resultado]
        
        return jsonify({
            'success': True,
            'marcas': marcas
        }), 200
    
    except Exception as e:
        print(f"Error al listar marcas: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@coches_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    Endpoint PÚBLICO para obtener estadísticas básicas
    No requiere autenticación
    """
    try:
        query = """
            SELECT 
                COUNT(*) as total_coches,
                MIN(precio) as precio_min,
                MAX(precio) as precio_max,
                AVG(precio) as precio_promedio,
                MIN(año) as año_min,
                MAX(año) as año_max
            FROM coches
        """
        resultado = execute_query(query, fetch=True)
        
        if not resultado:
            return jsonify({
                'success': False,
                'message': 'Error al obtener estadísticas'
            }), 500
        
        stats = resultado[0]
        if stats['precio_promedio']:
            stats['precio_promedio'] = float(stats['precio_promedio'])
        if stats['precio_min']:
            stats['precio_min'] = float(stats['precio_min'])
        if stats['precio_max']:
            stats['precio_max'] = float(stats['precio_max'])
        
        return jsonify({
            'success': True,
            'estadisticas': stats
        }), 200
    
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@coches_bp.route('/uploads/<filename>', methods=['GET'])
def servir_imagen(filename):
    """
    Endpoint PÚBLICO para servir imágenes
    Valida el nombre del archivo para prevenir path traversal
    """
    try:
        # Validar filename (prevenir path traversal)
        filename = secure_filename(filename)
        
        # Verificar que el archivo existe
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'Imagen no encontrada'
            }), 404
        
        from flask import send_from_directory
        return send_from_directory(UPLOAD_FOLDER, filename)
    
    except Exception as e:
        print(f"Error al servir imagen: {e}")
        return jsonify({
            'success': False,
            'message': 'Error al cargar la imagen'
        }), 500

# ============================================
# ENDPOINTS PROTEGIDOS (solo administradores)
# ============================================

@coches_bp.route('/coches', methods=['POST'])
@requiere_admin
def crear_coche():
    """
    PROTEGIDO: Solo administradores pueden crear coches
    Requiere token JWT válido con rol 'admin'
    """
    try:
        # Obtener datos del JSON
        data = request.get_json()
        marca = data.get('marca', '').strip()
        modelo = data.get('modelo', '').strip()
        año = data.get('año')
        precio = data.get('precio')
        descripcion = data.get('descripcion', '').strip()
        imagen_base64 = data.get('imagen', '')
        
        # Validar datos obligatorios
        if not marca or not modelo or not año or not precio:
            return jsonify({
                'success': False,
                'message': 'Marca, modelo, año y precio son obligatorios'
            }), 400
        
        # Validar tipos y rangos
        try:
            año = int(año)
            precio = float(precio)
            
            # Validaciones de negocio
            if año < 1900 or año > 2030:
                return jsonify({
                    'success': False,
                    'message': 'El año debe estar entre 1900 y 2030'
                }), 400
            
            if precio < 0 or precio > 1000000:
                return jsonify({
                    'success': False,
                    'message': 'El precio debe estar entre 0 y 1,000,000'
                }), 400
                
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Año y precio deben ser números válidos'
            }), 400
        
        # Guardar imagen si se proporciona
        imagen_filename = None
        if imagen_base64 and imagen_base64 != 'keep_current':
            try:
                # Extraer el contenido base64
                if ',' in imagen_base64:
                    imagen_base64 = imagen_base64.split(',')[1]
                
                # Validar tamaño
                imagen_data = base64.b64decode(imagen_base64)
                if len(imagen_data) > MAX_FILE_SIZE:
                    return jsonify({
                        'success': False,
                        'message': f'La imagen excede el tamaño máximo de {MAX_FILE_SIZE / 1024 / 1024}MB'
                    }), 400
                
                # Generar nombre seguro
                import time
                imagen_filename = secure_filename(f"coche_{int(time.time())}.jpg")
                imagen_path = os.path.join(UPLOAD_FOLDER, imagen_filename)
                
                # Guardar archivo
                with open(imagen_path, 'wb') as f:
                    f.write(imagen_data)
                    
            except Exception as e:
                print(f"Error al guardar imagen: {e}")
                return jsonify({
                    'success': False,
                    'message': 'Error al procesar la imagen'
                }), 400
        
        # Insertar coche
        query = """
            INSERT INTO coches (marca, modelo, año, precio, descripcion, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = execute_query(query, (marca, modelo, año, precio, descripcion, imagen_filename))
        
        if result and result['affected_rows'] > 0:
            # Log de auditoría
            print(f"AUDIT: Admin {request.user_email} creó coche ID {result['last_id']}")
            
            return jsonify({
                'success': True,
                'message': 'Coche creado exitosamente',
                'coche_id': result['last_id']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Error al crear coche'
            }), 500
    
    except Exception as e:
        print(f"Error al crear coche: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@coches_bp.route('/coches/<int:id>', methods=['PUT'])
@requiere_admin
def editar_coche(id):
    """
    PROTEGIDO: Solo administradores pueden editar coches
    Requiere token JWT válido con rol 'admin'
    """
    try:
        # Validar ID
        if id <= 0:
            return jsonify({
                'success': False,
                'message': 'ID inválido'
            }), 400
        
        # Verificar que el coche existe
        query_check = "SELECT imagen FROM coches WHERE id = %s"
        existe = execute_query(query_check, (id,), fetch=True)
        if not existe:
            return jsonify({
                'success': False,
                'message': 'Coche no encontrado'
            }), 404
        
        imagen_anterior = existe[0]['imagen']
        
        # Obtener datos
        data = request.get_json()
        marca = data.get('marca', '').strip()
        modelo = data.get('modelo', '').strip()
        año = data.get('año')
        precio = data.get('precio')
        descripcion = data.get('descripcion', '').strip()
        imagen_base64 = data.get('imagen', '')
        
        # Validar datos
        if not marca or not modelo or not año or not precio:
            return jsonify({
                'success': False,
                'message': 'Marca, modelo, año y precio son obligatorios'
            }), 400
        
        # Validar tipos y rangos
        try:
            año = int(año)
            precio = float(precio)
            
            if año < 1900 or año > 2030:
                return jsonify({
                    'success': False,
                    'message': 'El año debe estar entre 1900 y 2030'
                }), 400
            
            if precio < 0 or precio > 1000000:
                return jsonify({
                    'success': False,
                    'message': 'El precio debe estar entre 0 y 1,000,000'
                }), 400
                
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Año y precio deben ser números válidos'
            }), 400
        
        # Guardar nueva imagen si se proporciona
        imagen_filename = imagen_anterior
        if imagen_base64 and imagen_base64 != 'keep_current':
            try:
                if ',' in imagen_base64:
                    imagen_base64 = imagen_base64.split(',')[1]
                
                imagen_data = base64.b64decode(imagen_base64)
                if len(imagen_data) > MAX_FILE_SIZE:
                    return jsonify({
                        'success': False,
                        'message': f'La imagen excede el tamaño máximo de {MAX_FILE_SIZE / 1024 / 1024}MB'
                    }), 400
                
                import time
                imagen_filename = secure_filename(f"coche_{int(time.time())}.jpg")
                imagen_path = os.path.join(UPLOAD_FOLDER, imagen_filename)
                
                with open(imagen_path, 'wb') as f:
                    f.write(imagen_data)
                
                # Eliminar imagen anterior
                if imagen_anterior and imagen_anterior != 'default-car.jpg':
                    try:
                        os.remove(os.path.join(UPLOAD_FOLDER, imagen_anterior))
                    except:
                        pass
                        
            except Exception as e:
                print(f"Error al guardar imagen: {e}")
        
        # Actualizar coche
        query = """
            UPDATE coches 
            SET marca = %s, modelo = %s, año = %s, precio = %s, descripcion = %s, imagen = %s
            WHERE id = %s
        """
        result = execute_query(query, (marca, modelo, año, precio, descripcion, imagen_filename, id))
        
        if result and result['affected_rows'] > 0:
            # Log de auditoría
            print(f"AUDIT: Admin {request.user_email} editó coche ID {id}")
            
            return jsonify({
                'success': True,
                'message': 'Coche actualizado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al actualizar coche'
            }), 500
    
    except Exception as e:
        print(f"Error al editar coche: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@coches_bp.route('/coches/<int:id>', methods=['DELETE'])
@requiere_admin
def eliminar_coche(id):
    """
    PROTEGIDO: Solo administradores pueden eliminar coches
    Requiere token JWT válido con rol 'admin'
    """
    try:
        # Validar ID
        if id <= 0:
            return jsonify({
                'success': False,
                'message': 'ID inválido'
            }), 400
        
        # Verificar que el coche existe y obtener su imagen
        query_check = "SELECT imagen FROM coches WHERE id = %s"
        existe = execute_query(query_check, (id,), fetch=True)
        if not existe:
            return jsonify({
                'success': False,
                'message': 'Coche no encontrado'
            }), 404
        
        imagen = existe[0]['imagen']
        
        # Eliminar coche
        query = "DELETE FROM coches WHERE id = %s"
        result = execute_query(query, (id,))
        
        if result and result['affected_rows'] > 0:
            # Eliminar imagen del servidor
            if imagen and imagen != 'default-car.jpg':
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, imagen))
                except:
                    pass
            
            # Log de auditoría
            print(f"AUDIT: Admin {request.user_email} eliminó coche ID {id}")
            
            return jsonify({
                'success': True,
                'message': 'Coche eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al eliminar coche'
            }), 500
    
    except Exception as e:
        print(f"Error al eliminar coche: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500