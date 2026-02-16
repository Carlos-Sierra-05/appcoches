# Backend API de Coches - Python Flask

## 📋 Descripción

Backend sencillo en Python con Flask para gestionar una aplicación de coches. Incluye registro, login y listado de coches con filtros.

## 🗂️ Estructura del Proyecto

```
.
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración de base de datos
├── database.py         # Gestión de conexión a MySQL
├── registro.py         # Endpoint de registro de usuarios
├── login.py            # Endpoint de inicio de sesión
├── coches.py           # Endpoints de gestión de coches
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## 🚀 Instalación

### 1. Instalar Python
Asegúrate de tener Python 3.8 o superior instalado.

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos
Edita el archivo `config.py` y configura tu conexión a MySQL:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Tu usuario de MySQL
    'password': '',          # Tu contraseña de MySQL
    'database': 'appcoches',
    'charset': 'utf8mb4'
}
```

### 4. Ejecutar el servidor
```bash
python app.py
```

El servidor se iniciará en: `http://localhost:5000`

## 📡 Endpoints Disponibles

### 🔐 Autenticación

#### Registrar Usuario
```
POST /api/registro
Content-Type: application/json

Body:
{
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "password": "contraseña123"
}

Respuesta:
{
    "success": true,
    "message": "Usuario registrado exitosamente",
    "user_id": 1
}
```

#### Iniciar Sesión
```
POST /api/login
Content-Type: application/json

Body:
{
    "email": "juan@ejemplo.com",
    "password": "contraseña123"
}

Respuesta:
{
    "success": true,
    "message": "Inicio de sesión exitoso",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "usuario": {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@ejemplo.com",
        "rol": "usuario"
    }
}
```

#### Verificar Token
```
GET /api/verificar-token
Authorization: Bearer {token}

Respuesta:
{
    "success": true,
    "usuario": {
        "id": 1,
        "email": "juan@ejemplo.com",
        "rol": "usuario"
    }
}
```

### 🚗 Coches

#### Listar Coches (con filtros opcionales)
```
GET /api/coches?marca=Toyota&precio_min=10000&precio_max=20000&ordenar=precio&orden=ASC

Parámetros opcionales:
- marca: filtrar por marca (búsqueda parcial)
- modelo: filtrar por modelo (búsqueda parcial)
- año_min: año mínimo
- año_max: año máximo
- precio_min: precio mínimo
- precio_max: precio máximo
- ordenar: campo para ordenar (marca, modelo, año, precio)
- orden: ASC o DESC

Respuesta:
{
    "success": true,
    "total": 2,
    "coches": [
        {
            "id": 1,
            "marca": "Toyota",
            "modelo": "Corolla",
            "año": 2020,
            "precio": 15000.00,
            "descripcion": "Sedán compacto..."
        }
    ]
}
```

#### Obtener Coche por ID
```
GET /api/coches/1

Respuesta:
{
    "success": true,
    "coche": {
        "id": 1,
        "marca": "Toyota",
        "modelo": "Corolla",
        "año": 2020,
        "precio": 15000.00,
        "descripcion": "Sedán compacto..."
    }
}
```

#### Listar Marcas Disponibles
```
GET /api/marcas

Respuesta:
{
    "success": true,
    "marcas": ["BMW", "Ford", "Seat", "Toyota", "Volkswagen"]
}
```

#### Obtener Estadísticas
```
GET /api/estadisticas

Respuesta:
{
    "success": true,
    "estadisticas": {
        "total_coches": 5,
        "precio_min": 12000.00,
        "precio_max": 35000.00,
        "precio_promedio": 18800.00,
        "año_min": 2018,
        "año_max": 2022
    }
}
```

## 🔒 Seguridad

- Las contraseñas se encriptan con SHA-256 antes de almacenarse
- Se usa JWT (JSON Web Tokens) para la autenticación
- Los tokens expiran después de 24 horas
- CORS habilitado para permitir peticiones del frontend

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web
- **MySQL**: Base de datos
- **JWT**: Autenticación con tokens
- **Flask-CORS**: Manejo de CORS

## 📝 Notas

- En producción, cambia el `SECRET_KEY` en `config.py`
- Considera usar variables de entorno para las credenciales
- El token JWT se debe enviar en el header `Authorization: Bearer {token}`

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica que MySQL esté corriendo
- Comprueba las credenciales en `config.py`
- Asegúrate de que la base de datos `appcoches` existe

### Error al instalar mysql-connector-python
```bash
pip install mysql-connector-python --upgrade
```

### Puerto 5000 ocupado
Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
