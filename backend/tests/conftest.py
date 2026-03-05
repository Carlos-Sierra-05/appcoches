# tests/conftest.py
# Configuración de pytest y fixtures compartidas

import pytest
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from config import DB_CONFIG

# ============================================
# FIXTURES GENERALES
# ============================================

@pytest.fixture
def app():
    """
    Fixture que proporciona la aplicación Flask configurada para tests
    """
    flask_app.config['TESTING'] = True
    flask_app.config['DEBUG'] = False
    return flask_app

@pytest.fixture
def client(app):
    """
    Fixture que proporciona un cliente de test para hacer peticiones HTTP
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Fixture que proporciona un runner CLI para tests
    """
    return app.test_cli_runner()

# ============================================
# FIXTURES DE AUTENTICACIÓN
# ============================================

@pytest.fixture
def admin_token(client):
    """
    Fixture que devuelve un token JWT de administrador válido
    """
    response = client.post('/api/login',
                          json={
                              'email': 'admin@ejemplo.com',
                              'password': 'admin123'
                          },
                          content_type='application/json')
    
    if response.status_code == 200:
        data = response.get_json()
        return data.get('token')
    return None

@pytest.fixture
def user_token(client):
    """
    Fixture que devuelve un token JWT de usuario normal válido
    """
    # Primero registrar un usuario de test
    client.post('/api/registro',
               json={
                   'nombre': 'Usuario Test',
                   'email': 'usuario.test@test.com',
                   'password': 'Test1234'
               },
               content_type='application/json')
    
    # Luego hacer login
    response = client.post('/api/login',
                          json={
                              'email': 'usuario.test@test.com',
                              'password': 'Test1234'
                          },
                          content_type='application/json')
    
    if response.status_code == 200:
        data = response.get_json()
        return data.get('token')
    return None

@pytest.fixture
def auth_headers_admin(admin_token):
    """
    Fixture que devuelve headers con token de admin
    """
    return {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def auth_headers_user(user_token):
    """
    Fixture que devuelve headers con token de usuario
    """
    return {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }

# ============================================
# FIXTURES DE DATOS DE PRUEBA
# ============================================

@pytest.fixture
def sample_coche():
    """
    Fixture que devuelve datos de un coche de prueba
    """
    return {
        'marca': 'Toyota',
        'modelo': 'Corolla Test',
        'año': 2023,
        'precio': 20000.50,
        'descripcion': 'Coche de prueba para tests unitarios'
    }

@pytest.fixture
def sample_usuario():
    """
    Fixture que devuelve datos de un usuario de prueba
    """
    return {
        'nombre': 'Test User',
        'email': 'test.unique@example.com',
        'password': 'Test1234'
    }

# ============================================
# CONFIGURACIÓN DE PYTEST
# ============================================

def pytest_configure(config):
    """
    Configuración inicial de pytest
    """
    config.addinivalue_line(
        "markers", "slow: marca tests que son lentos"
    )
    config.addinivalue_line(
        "markers", "auth: marca tests relacionados con autenticación"
    )
    config.addinivalue_line(
        "markers", "security: marca tests de seguridad"
    )
    config.addinivalue_line(
        "markers", "integration: marca tests de integración"
    )
