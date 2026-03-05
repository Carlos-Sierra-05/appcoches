# tests/test_auth.py
# Tests de autenticación (registro, login, tokens)

import pytest
import json

# ============================================
# TESTS DE REGISTRO
# ============================================

@pytest.mark.auth
class TestRegistro:
    """Tests para el endpoint de registro"""
    
    def test_registro_exitoso(self, client):
        """Test: Registro con datos válidos debe ser exitoso"""
        response = client.post('/api/registro',
                              json={
                                  'nombre': 'Nuevo Usuario',
                                  'email': 'nuevo.usuario@test.com',
                                  'password': 'Password123'
                              })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] == True
        assert 'user_id' in data
    
    def test_registro_campos_vacios(self, client):
        """Test: Registro sin campos debe fallar"""
        response = client.post('/api/registro', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
    
    def test_registro_email_invalido(self, client):
        """Test: Registro con email inválido debe fallar"""
        response = client.post('/api/registro',
                              json={
                                  'nombre': 'Test',
                                  'email': 'email-invalido',
                                  'password': 'Test1234'
                              })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
        assert 'email' in data['message'].lower()
    
    def test_registro_password_debil(self, client):
        """Test: Registro con contraseña débil debe fallar"""
        response = client.post('/api/registro',
                              json={
                                  'nombre': 'Test',
                                  'email': 'test@test.com',
                                  'password': '123'  # Muy corta
                              })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
        assert 'contraseña' in data['message'].lower() or 'password' in data['message'].lower()
    
    def test_registro_password_sin_mayuscula(self, client):
        """Test: Contraseña sin mayúscula debe fallar"""
        response = client.post('/api/registro',
                              json={
                                  'nombre': 'Test',
                                  'email': 'test2@test.com',
                                  'password': 'test1234'  # Sin mayúscula
                              })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
    
    def test_registro_password_sin_numero(self, client):
        """Test: Contraseña sin número debe fallar"""
        response = client.post('/api/registro',
                              json={
                                  'nombre': 'Test',
                                  'email': 'test3@test.com',
                                  'password': 'TestTest'  # Sin número
                              })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
    
    def test_registro_email_duplicado(self, client):
        """Test: Registro con email existente debe fallar"""
        email = 'duplicado@test.com'
        
        # Primer registro
        client.post('/api/registro',
                   json={
                       'nombre': 'Usuario 1',
                       'email': email,
                       'password': 'Test1234'
                   })
        
        # Segundo registro con mismo email
        response = client.post('/api/registro',
                              json={
                                  'nombre': 'Usuario 2',
                                  'email': email,
                                  'password': 'Test1234'
                              })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
        assert 'registrado' in data['message'].lower()

# ============================================
# TESTS DE LOGIN
# ============================================

@pytest.mark.auth
class TestLogin:
    """Tests para el endpoint de login"""
    
    def test_login_exitoso(self, client):
        """Test: Login con credenciales válidas debe ser exitoso"""
        # Primero registrar usuario
        client.post('/api/registro',
                   json={
                       'nombre': 'Usuario Login',
                       'email': 'login@test.com',
                       'password': 'Login1234'
                   })
        
        # Luego hacer login
        response = client.post('/api/login',
                              json={
                                  'email': 'login@test.com',
                                  'password': 'Login1234'
                              })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'token' in data
        assert 'usuario' in data
    
    def test_login_credenciales_incorrectas(self, client):
        """Test: Login con contraseña incorrecta debe fallar"""
        response = client.post('/api/login',
                              json={
                                  'email': 'admin@ejemplo.com',
                                  'password': 'contraseña_incorrecta'
                              })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_login_usuario_inexistente(self, client):
        """Test: Login con usuario inexistente debe fallar"""
        response = client.post('/api/login',
                              json={
                                  'email': 'noexiste@test.com',
                                  'password': 'Password123'
                              })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_login_campos_vacios(self, client):
        """Test: Login sin credenciales debe fallar"""
        response = client.post('/api/login', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] == False
    
    def test_login_retorna_token_jwt(self, client):
        """Test: Login exitoso debe retornar token JWT válido"""
        response = client.post('/api/login',
                              json={
                                  'email': 'admin@ejemplo.com',
                                  'password': 'admin123'
                              })
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'token' in data
            # Verificar que el token tiene el formato correcto (JWT tiene 3 partes)
            token = data['token']
            assert len(token.split('.')) == 3

# ============================================
# TESTS DE TOKENS
# ============================================

@pytest.mark.auth
class TestTokens:
    """Tests para verificación de tokens JWT"""
    
    def test_verificar_token_valido(self, client, admin_token):
        """Test: Verificar token válido debe ser exitoso"""
        if admin_token:
            response = client.get('/api/verificar-token',
                                 headers={'Authorization': f'Bearer {admin_token}'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] == True
            assert 'usuario' in data
    
    def test_verificar_token_sin_token(self, client):
        """Test: Verificar sin token debe fallar"""
        response = client.get('/api/verificar-token')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_verificar_token_invalido(self, client):
        """Test: Verificar con token inválido debe fallar"""
        response = client.get('/api/verificar-token',
                             headers={'Authorization': 'Bearer token_invalido'})
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_token_contiene_info_usuario(self, client, admin_token):
        """Test: Token debe contener información del usuario"""
        if admin_token:
            response = client.get('/api/verificar-token',
                                 headers={'Authorization': f'Bearer {admin_token}'})
            
            if response.status_code == 200:
                data = response.get_json()
                usuario = data['usuario']
                assert 'email' in usuario
                assert 'rol' in usuario

# ============================================
# TESTS DE SEGURIDAD (RATE LIMITING)
# ============================================

@pytest.mark.security
@pytest.mark.slow
class TestAccountLockout:
    """Tests para bloqueo de cuenta por intentos fallidos"""
    
    def test_bloqueo_despues_5_intentos(self, client):
        """Test: Cuenta debe bloquearse después de 5 intentos fallidos"""
        email = 'lockout@test.com'
        
        # 5 intentos fallidos
        for i in range(5):
            response = client.post('/api/login',
                                  json={
                                      'email': email,
                                      'password': 'wrong_password'
                                  })
        
        # 6to intento debe indicar bloqueo
        response = client.post('/api/login',
                              json={
                                  'email': email,
                                  'password': 'wrong_password'
                              })
        
        assert response.status_code == 429  # Too Many Requests
        data = response.get_json()
        assert 'bloqueada' in data['message'].lower() or 'locked' in data['message'].lower()
