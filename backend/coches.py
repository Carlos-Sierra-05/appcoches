# coches.py
# Gestión de coches (listar con filtros)

from flask import Blueprint, request, jsonify
from database import execute_query
import jwt
from config import SECRET_KEY
import os
import base64
from werkzeug.utils import secure_filename

coches_bp = Blueprint('coches', __name__)

# Configuración de subida de archivos
UPLOAD_FOLDER = 'uploads/coches'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verificar_admin(token):
    """Verifica si el usuario es admin"""
    try:
        if token.startswith('Bearer '):
            token = token[7:]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('rol') == 'admin', payload
    except:
        return False, None

@coches_bp.route('/coches', methods=['GET'])
def listar_coches():
    """
    Endpoint para listar coches con filtros opcionales
    Parámetros de query:
    - marca: filtrar por marca
    - modelo: filtrar por modelo
    - año_min: año mínimo
    - año_max: año máximo
    - precio_min: precio mínimo
    - precio_max: precio máximo
    - ordenar: campo por el que ordenar (marca, modelo, año, precio)
    - orden: ASC o DESC
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
        
        # Validar campo de ordenamiento
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
        
        # Formatear precios a 2 decimales
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
    """Obtiene los detalles de un coche específico"""
    try:
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
    """Obtiene la lista única de marcas disponibles"""
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
    """Obtiene estadísticas básicas de los coches"""
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
        # Formatear decimales
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

@coches_bp.route('/coches', methods=['POST'])
def crear_coche():
    """Crea un nuevo coche (solo admin)"""
    try:
        # Verificar token y rol admin
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        es_admin, payload = verificar_admin(token)
        if not es_admin:
            return jsonify({
                'success': False,
                'message': 'Solo administradores pueden crear coches'
            }), 403
        
        # Obtener datos del JSON
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
        
        # Validar tipos
        try:
            año = int(año)
            precio = float(precio)
        except:
            return jsonify({
                'success': False,
                'message': 'Año y precio deben ser números válidos'
            }), 400
        
        # Guardar imagen si se proporciona
        imagen_filename = None
        if imagen_base64:
            try:
                # Extraer el contenido base64 (quitar el prefijo data:image/...)
                if ',' in imagen_base64:
                    imagen_base64 = imagen_base64.split(',')[1]
                
                # Decodificar base64
                imagen_data = base64.b64decode(imagen_base64)
                
                # Generar nombre único para el archivo
                import time
                imagen_filename = f"coche_{int(time.time())}.jpg"
                imagen_path = os.path.join(UPLOAD_FOLDER, imagen_filename)
                
                # Guardar archivo
                with open(imagen_path, 'wb') as f:
                    f.write(imagen_data)
            except Exception as e:
                print(f"Error al guardar imagen: {e}")
                imagen_filename = None
        
        # Insertar coche
        query = """
            INSERT INTO coches (marca, modelo, año, precio, descripcion, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = execute_query(query, (marca, modelo, año, precio, descripcion, imagen_filename))
        
        if result and result['affected_rows'] > 0:
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
def editar_coche(id):
    """Edita un coche existente (solo admin)"""
    try:
        # Verificar token y rol admin
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        es_admin, payload = verificar_admin(token)
        if not es_admin:
            return jsonify({
                'success': False,
                'message': 'Solo administradores pueden editar coches'
            }), 403
        
        # Verificar que el coche existe
        query_check = "SELECT imagen FROM coches WHERE id = %s"
        existe = execute_query(query_check, (id,), fetch=True)
        if not existe:
            return jsonify({
                'success': False,
                'message': 'Coche no encontrado'
            }), 404
        
        imagen_anterior = existe[0]['imagen']
        
        # Obtener datos del coche
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
        
        # Validar tipos
        try:
            año = int(año)
            precio = float(precio)
        except:
            return jsonify({
                'success': False,
                'message': 'Año y precio deben ser números válidos'
            }), 400
        
        # Guardar nueva imagen si se proporciona
        imagen_filename = imagen_anterior  # Mantener la imagen anterior por defecto
        if imagen_base64 and imagen_base64 != 'keep_current':
            try:
                # Extraer el contenido base64
                if ',' in imagen_base64:
                    imagen_base64 = imagen_base64.split(',')[1]
                
                # Decodificar base64
                imagen_data = base64.b64decode(imagen_base64)
                
                # Generar nombre único para el archivo
                import time
                imagen_filename = f"coche_{int(time.time())}.jpg"
                imagen_path = os.path.join(UPLOAD_FOLDER, imagen_filename)
                
                # Guardar archivo
                with open(imagen_path, 'wb') as f:
                    f.write(imagen_data)
                
                # Eliminar imagen anterior si existe
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
def eliminar_coche(id):
    """Elimina un coche (solo admin)"""
    try:
        # Verificar token y rol admin
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        es_admin, payload = verificar_admin(token)
        if not es_admin:
            return jsonify({
                'success': False,
                'message': 'Solo administradores pueden eliminar coches'
            }), 403
        
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
            # Eliminar imagen del servidor si existe
            if imagen and imagen != 'default-car.jpg':
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, imagen))
                except:
                    pass
            
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

@coches_bp.route('/uploads/<filename>', methods=['GET'])
def servir_imagen(filename):
    """Sirve una imagen de coche"""
    try:
        from flask import send_from_directory
        return send_from_directory(UPLOAD_FOLDER, filename)
    except:
        # Si no se encuentra la imagen, devolver una imagen por defecto
        return jsonify({
            'success': False,
            'message': 'Imagen no encontrada'
        }), 404