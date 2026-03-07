# 🚗 AppCoches

Aplicación web full-stack para la gestión de un catálogo de coches con autenticación JWT, control de acceso basado en roles y protección contra vulnerabilidades OWASP Top 10:2025.

[![CI/CD](https://img.shields.io/badge/CI/CD-passing-brightgreen)](https://github.com)
[![Security](https://img.shields.io/badge/OWASP-Top%2010%20Protected-blue)](https://owasp.org)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

---

## 📸 Capturas de pantalla

### Login
![Login](ImagenesApp/Login.png)

### Registro
![Registro](Imagenes%20App/Registro.png)

### Vista Admin
![Vista Admin](Imagenes%20App/Admin.png)

### Añadir Coche
![Añadir Coche](Imagenes%20App/Añadir_Coche.png)

### Vista Usuario
![Vista Usuario](Imagenes%20App/Usuario.png)

---

## 📋 Características

- 🔐 **Autenticación JWT** con bcrypt y expiración de tokens
- 👥 **Roles de usuario** (Admin/Usuario) con control de acceso
- 🚗 **CRUD completo** de coches (solo admins)
- 🔍 **Filtros avanzados** por marca, modelo, año y precio
- 📊 **Estadísticas** del catálogo en tiempo real
- 📸 **Gestión de imágenes** con validación y almacenamiento
- 🛡️ **Seguridad OWASP** (Top 10:2025 compliant)
- 🐳 **Dockerizado** para fácil despliegue
- 🧪 **82 tests** automatizados con pytest
- 📝 **Logging de seguridad** completo

---

## 🛠️ Tecnologías

**Backend:**
- Python 3.11 + Flask
- MySQL 8.0
- JWT + bcrypt
- Flask-Limiter (rate limiting)

**Frontend:**
- HTML5 + CSS3 + JavaScript
- Diseño responsive moderno

**DevOps:**
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- Pytest (82 tests unitarios)

---

## 🚀 Inicio rápido

### Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <url-repositorio>
cd appcoches

# 2. Levantar contenedores
cd docker
docker-compose up -d

# 3. Acceder a la aplicación
# Frontend: http://localhost:8000/login.html
# Backend API: http://localhost:5000
```

### Sin Docker (Desarrollo local)

```bash
# 1. Instalar dependencias
cd backend
pip install -r requirements.txt

# 2. Configurar MySQL (XAMPP/WAMP)
# Ejecutar docker/init.sql en phpMyAdmin

# 3. Iniciar backend
python app.py

# 4. Iniciar frontend (en otra terminal)
cd frontend
python -m http.server 8000

# 5. Abrir http://localhost:8000/login.html
```

---

## 🔑 Credenciales por defecto

**Administrador:**
```
Email: admin@ejemplo.com
Password: admin123
```

---

## 📁 Estructura del proyecto

```
appcoches/
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD
│
├── backend/                  # API Flask
│   ├── tests/               # Tests unitarios (82)
│   │   ├── __init__.py
│   │   ├── conftest.py      # Configuración y fixtures
│   │   ├── test_auth.py     # Tests de autenticación (24)
│   │   ├── test_coches.py   # Tests de CRUD (20)
│   │   ├── test_security.py # Tests de seguridad (22)
│   │   └── test_api.py      # Tests generales (16)
│   ├── logs/                # Logs de seguridad
│   │   └── security.log
│   ├── uploads/             # Imágenes de coches
│   │   └── coches/
│   ├── app.py              # Aplicación principal
│   ├── config.py           # Configuración
│   ├── database.py         # Conexión MySQL
│   ├── login.py            # Autenticación
│   ├── registro.py         # Registro de usuarios
│   ├── coches.py           # CRUD de coches
│   ├── security_logger.py  # Sistema de logging
│   ├── pytest.ini          # Configuración pytest
│   └── requirements.txt    # Dependencias
│
├── frontend/                # Interfaz de usuario
│   ├── login.html          # Página de login
│   ├── registro.html       # Página de registro
│   └── coches.html         # Página principal
│
├── docker/                  # Configuración Docker
│   ├── Dockerfile          # Imagen de la aplicación
│   ├── docker-compose.yml  # Orquestación de contenedores
│   ├── init.sql            # BD inicial con datos
│   ├── start.sh            # Script de inicio
│   └── .dockerignore
│
├── Imagenes App/            # Capturas de pantalla
│   ├── Login.png
│   ├── Registro.png
│   ├── Admin.png
│   ├── Usuario.png
│   └── Añadir_Coche.png
│
├── README.md               # Este archivo
```

---

## 🌐 API Endpoints

### Públicos (sin autenticación)
```
GET  /                        # Información de la API
GET  /health                  # Health check
GET  /api/coches              # Listar coches (con filtros)
GET  /api/coches/:id          # Obtener un coche
GET  /api/marcas              # Lista de marcas
GET  /api/estadisticas        # Estadísticas del catálogo
GET  /api/uploads/:filename   # Obtener imagen
POST /api/registro            # Registrar usuario
POST /api/login               # Iniciar sesión
GET  /api/verificar-token     # Verificar token JWT
```

### Protegidos (requieren admin)
```
POST   /api/coches            # Crear coche
PUT    /api/coches/:id        # Editar coche
DELETE /api/coches/:id        # Eliminar coche
```

**Ejemplos de filtros:**
```
GET /api/coches?marca=BMW
GET /api/coches?precio_min=20000&precio_max=30000
GET /api/coches?año_min=2020
GET /api/coches?ordenar=precio&orden=DESC
GET /api/coches?marca=BMW&precio_min=20000&ordenar=año&orden=DESC
```

---

## 🧪 Tests

```bash
# Ejecutar todos los tests
cd backend
pytest

# Tests por categoría
pytest -m auth          # Tests de autenticación (24)
pytest -m security      # Tests de seguridad (22)
pytest tests/test_coches.py  # Tests de CRUD (20)

# Con cobertura
pytest --cov=. --cov-report=html

# Tests específicos
pytest tests/test_auth.py::TestRegistro::test_registro_exitoso
```

**Total: 82 tests automatizados** ✅

**Distribución:**
- 🔐 Autenticación: 24 tests
- 🚗 CRUD Coches: 20 tests
- 🛡️ Seguridad: 22 tests
- 🌐 API General: 16 tests

---

## 🛡️ Seguridad (OWASP Top 10:2025)

| Vulnerabilidad | Estado | Protección |
|----------------|--------|------------|
| **A01** - Broken Access Control | ✅ | Decoradores `@requiere_admin`, verificación de roles |
| **A02** - Security Misconfiguration | ✅ | Headers de seguridad (HSTS, CSP, etc.), debug controlado |
| **A03** - Supply Chain Failures | ✅ | Versiones fijas en requirements.txt |
| **A04** - Cryptographic Failures | ✅ | bcrypt (12 rondas), tokens JWT con expiración |
| **A05** - Injection | ✅ | Queries parametrizadas, validación de entrada |
| **A06** - Insecure Design | ✅ | Rate limiting, validaciones robustas |
| **A07** - Authentication Failures | ✅ | Bloqueo de cuenta (5 intentos), contraseñas robustas |
| **A08** - Data Integrity Failures | ✅ | Validación de archivos, límites de tamaño |
| **A09** - Logging Failures | ✅ | Sistema completo de logs de seguridad |
| **A10** - Exception Handling | ✅ | Manejadores de error centralizados |

---

## 🐳 Comandos Docker

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f app
docker-compose logs -f db

# Detener
docker-compose down

# Detener y eliminar volúmenes (¡borra la BD!)
docker-compose down -v

# Reiniciar
docker-compose restart

# Reconstruir
docker-compose up --build

# Ver estado
docker-compose ps

# Acceder al contenedor
docker exec -it appcoches-app bash
docker exec -it appcoches-mysql mysql -u root -pAppCoches9393 appcoches
```

---

## 📊 Base de datos

### Tablas principales

**usuarios**
- `id` - ID único
- `nombre` - Nombre completo
- `email` - Email único
- `password` - Contraseña (bcrypt)
- `rol` - admin / usuario
- `fecha_registro` - Timestamp

**coches**
- `id` - ID único
- `marca` - Marca del coche
- `modelo` - Modelo del coche
- `año` - Año de fabricación
- `precio` - Precio en euros
- `descripcion` - Descripción detallada
- `imagen` - Nombre del archivo de imagen

### Datos iniciales

- **2 usuarios**: 1 admin + 1 usuario normal
- **12 coches** de ejemplo (Audi, BMW, Mercedes, Volvo, VW, Seat, Opel)

---

## 🔧 Configuración

### Variables de entorno (opcional)

Crear archivo `.env` en `backend/`:

```env
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=appcoches

# Seguridad
SECRET_KEY=tu_clave_secreta_aqui
JWT_EXPIRATION_HOURS=2

# CORS
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000

# Rate Limiting
RATE_LIMIT_LOGIN=5 per minute
RATE_LIMIT_REGISTER=3 per hour
RATE_LIMIT_API=100 per minute

# Logging
LOG_LEVEL=INFO
```

---

## 🚨 Solución de problemas

### Puerto ocupado
```bash
# Detener XAMPP/WAMP antes de usar Docker
# O cambiar puertos en docker-compose.yml
```

### Error de conexión MySQL
```bash
# Verificar que MySQL esté corriendo
docker-compose logs db

# Esperar a que MySQL inicialice (primera vez tarda ~30s)
```

### Logs no se crean
```bash
# Verificar que la carpeta logs/ existe
mkdir backend/logs

# Verificar permisos
chmod 755 backend/logs
```

### Token expirado
```
# Los tokens expiran en 2 horas
# Vuelve a hacer login para obtener uno nuevo
```

### Tests fallan
```bash
# Verificar que estés en backend/
cd backend
pytest

# Instalar dependencias de tests
pip install pytest pytest-cov
```

### Imágenes no se ven
```bash
# Verificar que la carpeta existe
mkdir -p backend/uploads/coches

# Verificar permisos
chmod 755 backend/uploads/coches
```

---

## 🔄 CI/CD con GitHub Actions

El proyecto incluye integración continua automatizada:

**Ubicación:** `.github/workflows/ci-cd.yml`

**Jobs ejecutados:**
1. ✅ Validar sintaxis Python (flake8)
2. ✅ Ejecutar 82 tests unitarios
3. ✅ Validar estructura del proyecto
4. ✅ Escaneo de seguridad (Safety + Bandit)

**Se ejecuta en:**
- Push a `main`, `master`, `develop`
- Pull Requests

**Ver resultados:** Pestaña "Actions" en GitHub

---

## 📚 Documentación adicional

- **[SEGURIDAD_OWASP.md](SEGURIDAD_OWASP.md)** - Detalles completos de protecciones OWASP
- **[GITHUB_ACTIONS.md](GITHUB_ACTIONS.md)** - Guía completa de CI/CD
- **[TESTS_README.md](TESTS_README.md)** - Documentación de tests y fixtures
- **[POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)** - Colección de Postman con ejemplos

---

## 📖 Casos de uso

### Usuario normal:
1. Registrarse en la aplicación
2. Iniciar sesión
3. Ver catálogo de coches
4. Filtrar por marca, modelo, precio, año
5. Ver detalles de cada coche
6. Ver estadísticas del catálogo

### Administrador:
1. Todo lo anterior +
2. Añadir nuevos coches con imagen
3. Editar información de coches existentes
4. Cambiar imágenes de coches
5. Eliminar coches del catálogo
6. Badge "ADMIN" visible en la interfaz

---

## 🎓 Proyecto académico

Desarrollado como proyecto académico para demostrar:
- ✅ Arquitectura cliente-servidor
- ✅ API RESTful con autenticación JWT
- ✅ CRUD completo con control de acceso
- ✅ Seguridad según OWASP Top 10:2025
- ✅ Dockerización de aplicaciones
- ✅ Testing automatizado con pytest
- ✅ CI/CD con GitHub Actions
- ✅ Logging y auditoría de seguridad

---

## 🔐 Características de seguridad implementadas

- 🔒 **Contraseñas**: bcrypt con 12 rondas
- 🎫 **Tokens**: JWT con expiración de 2 horas
- 🚫 **Rate Limiting**: 5 intentos de login, 100 peticiones/min API
- 🔓 **Bloqueo de cuenta**: 5 intentos fallidos = 15 min bloqueado
- 🛡️ **Headers**: HSTS, CSP, X-Frame-Options, etc.
- 📝 **Logs**: Registro completo de eventos de seguridad
- ✅ **Validaciones**: Email, contraseñas robustas, tipos de archivo
- 🔍 **SQL Injection**: Queries parametrizadas
- 🎭 **Roles**: Control de acceso basado en roles (RBAC)

---

**🚀 ¡Listo para usar!** 

Accede a **[http://localhost:8000/login.html](http://localhost:8000/login.html)** después de iniciar la aplicación.