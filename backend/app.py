# app.py
# Aplicación principal Flask

from flask import Flask, jsonify
from flask_cors import CORS
from registro import registro_bp
from login import login_bp
from coches import coches_bp

# Crear aplicación Flask
app = Flask(__name__)

# Habilitar CORS para permitir peticiones desde el frontend
CORS(app)

# Registrar blueprints (rutas)
app.register_blueprint(registro_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(coches_bp, url_prefix='/api')

# Ruta de inicio
@app.route('/')
def inicio():
    return jsonify({
        'message': 'API de Coches funcionando correctamente',
        'version': '1.0',
        'endpoints': {
            'registro': '/api/registro (POST)',
            'login': '/api/login (POST)',
            'verificar_token': '/api/verificar-token (GET)',
            'listar_coches': '/api/coches (GET)',
            'obtener_coche': '/api/coches/<id> (GET)',
            'marcas': '/api/marcas (GET)',
            'estadisticas': '/api/estadisticas (GET)'
        }
    })

# Manejador de errores 404
@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint no encontrado'
    }), 404

# Manejador de errores 500
@app.errorhandler(500)
def error_servidor(error):
    return jsonify({
        'success': False,
        'message': 'Error interno del servidor'
    }), 500

# Ejecutar aplicación
if __name__ == '__main__':
    print("=" * 50)
    print("Servidor Flask iniciado")
    print("API disponible en: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
