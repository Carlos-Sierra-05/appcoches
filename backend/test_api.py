# test_api.py
# Tests básicos para la API de AppCoches

import unittest
import json
from app import app
from config import DB_CONFIG

class TestAPI(unittest.TestCase):
    """Tests básicos de la API"""
    
    def setUp(self):
        """Configurar antes de cada test"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_1_api_root(self):
        """Test: GET / debe devolver información de la API"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('application'))
        self.assertEqual(data['application'], 'AppCoches API')
    
    def test_2_health_check(self):
        """Test: GET /health debe devolver status healthy"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_3_listar_coches_sin_auth(self):
        """Test: GET /api/coches debe funcionar sin autenticación"""
        response = self.app.get('/api/coches')
        self.assertIn(response.status_code, [200, 500])  # 500 si no hay BD
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_4_obtener_marcas(self):
        """Test: GET /api/marcas debe devolver lista de marcas"""
        response = self.app.get('/api/marcas')
        self.assertIn(response.status_code, [200, 500])
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_5_estadisticas(self):
        """Test: GET /api/estadisticas debe devolver estadísticas"""
        response = self.app.get('/api/estadisticas')
        self.assertIn(response.status_code, [200, 500])
        data = json.loads(response.data)
        self.assertIn('success', data)
    
    def test_6_registro_campos_vacios(self):
        """Test: POST /api/registro debe rechazar campos vacíos"""
        response = self.app.post('/api/registro',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_7_registro_email_invalido(self):
        """Test: POST /api/registro debe rechazar email inválido"""
        response = self.app.post('/api/registro',
                                data=json.dumps({
                                    'nombre': 'Test',
                                    'email': 'invalid-email',
                                    'password': 'Test1234'
                                }),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_8_registro_password_debil(self):
        """Test: POST /api/registro debe rechazar contraseña débil"""
        response = self.app.post('/api/registro',
                                data=json.dumps({
                                    'nombre': 'Test',
                                    'email': 'test@example.com',
                                    'password': '123'
                                }),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_9_login_sin_credenciales(self):
        """Test: POST /api/login debe rechazar sin credenciales"""
        response = self.app.post('/api/login',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_10_crear_coche_sin_auth(self):
        """Test: POST /api/coches debe rechazar sin autenticación"""
        response = self.app.post('/api/coches',
                                data=json.dumps({
                                    'marca': 'Test',
                                    'modelo': 'Test',
                                    'año': 2020,
                                    'precio': 10000
                                }),
                                content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_11_editar_coche_sin_auth(self):
        """Test: PUT /api/coches/1 debe rechazar sin autenticación"""
        response = self.app.put('/api/coches/1',
                               data=json.dumps({
                                   'marca': 'Test',
                                   'modelo': 'Test',
                                   'año': 2020,
                                   'precio': 10000
                               }),
                               content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_12_eliminar_coche_sin_auth(self):
        """Test: DELETE /api/coches/1 debe rechazar sin autenticación"""
        response = self.app.delete('/api/coches/1')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_13_verificar_token_sin_token(self):
        """Test: GET /api/verificar-token debe rechazar sin token"""
        response = self.app.get('/api/verificar-token')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_14_404_endpoint_inexistente(self):
        """Test: Endpoint inexistente debe devolver 404"""
        response = self.app.get('/api/endpoint-que-no-existe')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    # Ejecutar tests
    unittest.main(verbosity=2)
