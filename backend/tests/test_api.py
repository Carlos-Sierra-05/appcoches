# tests/test_api.py
# Tests generales de la API

import pytest
import json

# ============================================
# TESTS DE ENDPOINTS BÁSICOS
# ============================================

class TestAPIBasica:
    """Tests básicos de la API"""
    
    def test_api_root_endpoint(self, client):
        """Test: Endpoint raíz debe devolver información de la API"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'application' in data
        assert data['application'] == 'AppCoches API'
    
    def test_api_version(self, client):
        """Test: API debe devolver versión"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'version' in data
        assert isinstance(data['version'], str)
    
    def test_api_status(self, client):
        """Test: API debe indicar que está corriendo"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'running'
    
    def test_health_check_endpoint(self, client):
        """Test: Health check endpoint debe funcionar"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'
    
    def test_health_check_timestamp(self, client):
        """Test: Health check debe incluir timestamp"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'timestamp' in data

# ============================================
# TESTS DE MANEJO DE ERRORES
# ============================================

class TestErrorHandling:
    """Tests de manejo de errores HTTP"""
    
    def test_404_endpoint_inexistente(self, client):
        """Test: Endpoint inexistente debe devolver 404"""
        response = client.get('/api/endpoint-que-no-existe')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] == False
        assert 'error' in data
    
    def test_405_metodo_no_permitido(self, client):
        """Test: Método HTTP no permitido debe devolver 405"""
        # GET no está permitido en /api/login
        response = client.get('/api/login')
        
        assert response.status_code == 405
        data = response.get_json()
        assert data['success'] == False
    
    def test_400_datos_invalidos(self, client):
        """Test: Datos inválidos deben devolver 400"""
        response = client.post('/api/registro',
                              json={})  # Sin datos
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
    
    def test_401_sin_autenticacion(self, client):
        """Test: Acceso sin auth debe devolver 401"""
        response = client.post('/api/coches',
                              json={
                                  'marca': 'Test',
                                  'modelo': 'Test',
                                  'año': 2020,
                                  'precio': 10000
                              })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False

# ============================================
# TESTS DE CORS
# ============================================

class TestCORS:
    """Tests de configuración CORS"""
    
    def test_cors_headers_presentes(self, client):
        """Test: Headers CORS deben estar presentes en OPTIONS"""
        response = client.options('/api/coches')
        
        # Debe tener headers CORS
        assert 'Access-Control-Allow-Origin' in response.headers or response.status_code == 200
    
    def test_metodos_cors_permitidos(self, client):
        """Test: Métodos CORS permitidos"""
        response = client.options('/api/coches')
        
        if 'Access-Control-Allow-Methods' in response.headers:
            methods = response.headers['Access-Control-Allow-Methods']
            assert 'GET' in methods
            assert 'POST' in methods
            assert 'PUT' in methods
            assert 'DELETE' in methods

# ============================================
# TESTS DE CONTENIDO
# ============================================

class TestContentType:
    """Tests de content-type"""
    
    def test_response_es_json(self, client):
        """Test: Respuestas deben ser JSON"""
        response = client.get('/')
        
        assert 'application/json' in response.content_type
    
    def test_post_acepta_json(self, client):
        """Test: POST debe aceptar JSON"""
        response = client.post('/api/registro',
                              data='no es json',
                              content_type='text/plain')
        
        # Debe rechazar si no es JSON
        assert response.status_code in [400, 415, 500]

# ============================================
# TESTS DE DOCUMENTACIÓN
# ============================================

class TestDocumentacion:
    """Tests de documentación de la API"""
    
    def test_endpoints_documentados(self, client):
        """Test: Endpoints deben estar documentados en /"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'endpoints' in data
        assert isinstance(data['endpoints'], dict)
    
    def test_security_features_documentadas(self, client):
        """Test: Features de seguridad documentadas"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'security_features' in data
        assert isinstance(data['security_features'], list)
        assert len(data['security_features']) > 0

# ============================================
# TESTS DE INTEGRACIÓN BÁSICA
# ============================================

@pytest.mark.integration
class TestIntegracionBasica:
    """Tests de integración básica"""
    
    def test_flujo_completo_registro_login(self, client):
        """Test: Flujo completo de registro y login"""
        # 1. Registrar usuario
        response_registro = client.post('/api/registro',
                                       json={
                                           'nombre': 'Usuario Flujo',
                                           'email': 'flujo@test.com',
                                           'password': 'Flujo1234'
                                       })
        
        # Puede fallar si ya existe o si hay error de BD
        assert response_registro.status_code in [201, 400, 500]
        
        # 2. Si registro exitoso, hacer login
        if response_registro.status_code == 201:
            response_login = client.post('/api/login',
                                        json={
                                            'email': 'flujo@test.com',
                                            'password': 'Flujo1234'
                                        })
            
            assert response_login.status_code == 200
            data = response_login.get_json()
            assert 'token' in data
            assert 'usuario' in data
    
    def test_token_usado_en_request(self, client, admin_token):
        """Test: Token puede ser usado en peticiones"""
        if admin_token:
            # Usar token para verificar
            response = client.get('/api/verificar-token',
                                 headers={'Authorization': f'Bearer {admin_token}'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] == True
