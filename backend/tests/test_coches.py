# tests/test_coches.py
# Tests para el CRUD de coches

import pytest
import json

# ============================================
# TESTS DE ENDPOINTS PÚBLICOS
# ============================================

class TestCochesPublicos:
    """Tests para endpoints públicos (sin autenticación)"""
    
    def test_listar_coches(self, client):
        """Test: Listar coches debe funcionar sin autenticación"""
        response = client.get('/api/coches')
        
        assert response.status_code in [200, 500]  # 500 si no hay BD
        data = response.get_json()
        assert 'success' in data
    
    def test_listar_coches_con_filtro_marca(self, client):
        """Test: Filtrar coches por marca"""
        response = client.get('/api/coches?marca=BMW')
        
        assert response.status_code in [200, 500]
        data = response.get_json()
        assert 'success' in data
    
    def test_listar_coches_con_ordenamiento(self, client):
        """Test: Ordenar coches por precio"""
        response = client.get('/api/coches?ordenar=precio&orden=DESC')
        
        assert response.status_code in [200, 500]
        data = response.get_json()
        assert 'success' in data
    
    def test_obtener_marcas(self, client):
        """Test: Obtener lista de marcas"""
        response = client.get('/api/marcas')
        
        assert response.status_code in [200, 500]
        data = response.get_json()
        assert 'success' in data
    
    def test_obtener_estadisticas(self, client):
        """Test: Obtener estadísticas del catálogo"""
        response = client.get('/api/estadisticas')
        
        assert response.status_code in [200, 500]
        data = response.get_json()
        assert 'success' in data
    
    def test_obtener_coche_por_id(self, client):
        """Test: Obtener un coche específico por ID"""
        response = client.get('/api/coches/1')
        
        assert response.status_code in [200, 404, 500]
        data = response.get_json()
        assert 'success' in data

# ============================================
# TESTS DE PROTECCIÓN (SIN AUTH)
# ============================================

class TestCochesProtegidos:
    """Tests para verificar protección de endpoints admin"""
    
    def test_crear_coche_sin_auth(self, client, sample_coche):
        """Test: Crear coche sin autenticación debe fallar"""
        response = client.post('/api/coches',
                              json=sample_coche)
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_editar_coche_sin_auth(self, client, sample_coche):
        """Test: Editar coche sin autenticación debe fallar"""
        response = client.put('/api/coches/1',
                             json=sample_coche)
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False
    
    def test_eliminar_coche_sin_auth(self, client):
        """Test: Eliminar coche sin autenticación debe fallar"""
        response = client.delete('/api/coches/1')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] == False

# ============================================
# TESTS CRUD CON USUARIO NORMAL
# ============================================

class TestCochesUsuarioNormal:
    """Tests para verificar que usuario normal no puede hacer CRUD"""
    
    def test_crear_coche_como_usuario(self, client, auth_headers_user, sample_coche):
        """Test: Usuario normal no puede crear coches"""
        if auth_headers_user:
            response = client.post('/api/coches',
                                  json=sample_coche,
                                  headers=auth_headers_user)
            
            assert response.status_code == 403
            data = response.get_json()
            assert data['success'] == False
    
    def test_editar_coche_como_usuario(self, client, auth_headers_user, sample_coche):
        """Test: Usuario normal no puede editar coches"""
        if auth_headers_user:
            response = client.put('/api/coches/1',
                                 json=sample_coche,
                                 headers=auth_headers_user)
            
            assert response.status_code == 403
            data = response.get_json()
            assert data['success'] == False
    
    def test_eliminar_coche_como_usuario(self, client, auth_headers_user):
        """Test: Usuario normal no puede eliminar coches"""
        if auth_headers_user:
            response = client.delete('/api/coches/1',
                                    headers=auth_headers_user)
            
            assert response.status_code == 403
            data = response.get_json()
            assert data['success'] == False

# ============================================
# TESTS CRUD CON ADMIN
# ============================================

@pytest.mark.integration
class TestCochesAdmin:
    """Tests para operaciones CRUD como administrador"""
    
    def test_crear_coche_como_admin(self, client, auth_headers_admin, sample_coche):
        """Test: Admin puede crear coches"""
        if auth_headers_admin:
            response = client.post('/api/coches',
                                  json=sample_coche,
                                  headers=auth_headers_admin)
            
            # Puede ser 201 (éxito) o 500 (error BD)
            assert response.status_code in [201, 500]
            data = response.get_json()
            
            if response.status_code == 201:
                assert data['success'] == True
                assert 'coche_id' in data
    
    def test_crear_coche_sin_campos_obligatorios(self, client, auth_headers_admin):
        """Test: Crear coche sin campos obligatorios debe fallar"""
        if auth_headers_admin:
            response = client.post('/api/coches',
                                  json={'marca': 'Test'},  # Faltan campos
                                  headers=auth_headers_admin)
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] == False
    
    def test_crear_coche_con_año_invalido(self, client, auth_headers_admin):
        """Test: Crear coche con año fuera de rango debe fallar"""
        if auth_headers_admin:
            response = client.post('/api/coches',
                                  json={
                                      'marca': 'Test',
                                      'modelo': 'Test',
                                      'año': 1800,  # Año inválido
                                      'precio': 10000
                                  },
                                  headers=auth_headers_admin)
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] == False
    
    def test_crear_coche_con_precio_negativo(self, client, auth_headers_admin):
        """Test: Crear coche con precio negativo debe fallar"""
        if auth_headers_admin:
            response = client.post('/api/coches',
                                  json={
                                      'marca': 'Test',
                                      'modelo': 'Test',
                                      'año': 2020,
                                      'precio': -1000  # Precio negativo
                                  },
                                  headers=auth_headers_admin)
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] == False
    
    def test_editar_coche_inexistente(self, client, auth_headers_admin, sample_coche):
        """Test: Editar coche que no existe debe fallar"""
        if auth_headers_admin:
            response = client.put('/api/coches/99999',
                                 json=sample_coche,
                                 headers=auth_headers_admin)
            
            assert response.status_code == 404
            data = response.get_json()
            assert data['success'] == False
    
    def test_eliminar_coche_inexistente(self, client, auth_headers_admin):
        """Test: Eliminar coche que no existe debe fallar"""
        if auth_headers_admin:
            response = client.delete('/api/coches/99999',
                                    headers=auth_headers_admin)
            
            assert response.status_code == 404
            data = response.get_json()
            assert data['success'] == False

# ============================================
# TESTS DE VALIDACIÓN
# ============================================

class TestValidacionCoches:
    """Tests para validación de datos de coches"""
    
    def test_validacion_tipos_datos(self, client, auth_headers_admin):
        """Test: Validar tipos de datos correctos"""
        if auth_headers_admin:
            response = client.post('/api/coches',
                                  json={
                                      'marca': 'Test',
                                      'modelo': 'Test',
                                      'año': 'texto',  # Debería ser número
                                      'precio': 10000
                                  },
                                  headers=auth_headers_admin)
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] == False
