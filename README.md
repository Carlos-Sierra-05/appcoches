# 🚗 AppCoches

Aplicación web full-stack para la gestión de un catálogo de coches con autenticación JWT, control de acceso basado en roles y protección contra vulnerabilidades OWASP Top 10:2025.

[![CI/CD](https://img.shields.io/badge/CI/CD-passing-brightgreen)](https://github.com)
[![Security](https://img.shields.io/badge/OWASP-Top%2010%20Protected-blue)](https://owasp.org)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

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

## 📁 Estructura del proyecto

```
appcoches/
├── backend/                  # API Flask
│   ├── tests/               # Tests unitarios (82)
│   ├── logs/                # Logs de seguridad
│   ├── uploads/             # Imágenes de coches
│   ├── app.py              # Aplicación principal
│   ├── config.py           # Configuración
│   ├── database.py         # Conexión MySQL
│   ├── login.py            # Autenticación
│   ├── registro.py         # Registro de usuarios
│   ├── coches.py           # CRUD de coches
│   ├── security_logger.py  # Sistema de logging
│   └── requirements.txt    # Dependencias
│
├── frontend/                # Interfaz de usuario
│   ├── login.html
│   ├── registro.html
│   └── coches.html
│
├── docker/                  # Configuración Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── init.sql            # BD inicial con datos
│   └── start.sh
│
└── README.md
```

---

## 🌐 API Endpoints

### Públicos (sin autenticación)
```
GET  /api/coches              # Listar coches (con filtros)
GET  /api/coches/:id          # Obtener un coche
GET  /api/marcas              # Lista de marcas
GET  /api/estadisticas        # Estadísticas del catálogo
POST /api/registro            # Registrar usuario
POST /api/login               # Iniciar sesión
```

### Protegidos (requieren admin)
```
POST   /api/coches            # Crear coche
PUT    /api/coches/:id        # Editar coche
DELETE /api/coches/:id        # Eliminar coche
```

**Filtros disponibles:**
- `?marca=BMW` - Filtrar por marca
- `?precio_min=20000` - Precio mínimo
- `?precio_max=30000` - Precio máximo
- `?año_min=2020` - Año mínimo
- `?ordenar=precio&orden=DESC` - Ordenar

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
```

**Total: 82 tests automatizados**

---

## 🛡️ Seguridad (OWASP Top 10:2025)

✅ **A01 - Broken Access Control:** Decoradores `@requiere_admin`, verificación de roles  
✅ **A02 - Security Misconfiguration:** Headers de seguridad (HSTS, CSP, etc.), debug mode controlado  
✅ **A03 - Supply Chain:** Versiones fijas en requirements.txt  
✅ **A04 - Cryptographic Failures:** bcrypt (12 rondas), tokens JWT con expiración  
✅ **A05 - Injection:** Queries parametrizadas, validación de entrada  
✅ **A06 - Insecure Design:** Rate limiting, validaciones robustas  
✅ **A07 - Authentication Failures:** Bloqueo de cuenta (5 intentos), contraseñas robustas  
✅ **A08 - Data Integrity:** Validación de archivos, límites de tamaño  
✅ **A09 - Logging Failures:** Sistema completo de logs de seguridad  
✅ **A10 - Exception Handling:** Manejadores de error centralizados  

---

## 🐳 Comandos Docker

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir
docker-compose up --build
```

---

## 📊 Base de datos

**Tablas:**
- `usuarios` - Usuarios del sistema (admin/usuario)
- `coches` - Catálogo de coches

**Datos iniciales:**
- 2 usuarios (1 admin, 1 usuario)
- 12 coches de ejemplo

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

# Rate Limiting
RATE_LIMIT_LOGIN=5 per minute
RATE_LIMIT_API=100 per minute
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
```

### Token expirado
```
# Los tokens expiran en 2 horas
# Vuelve a hacer login
```

### Tests fallan
```bash
# Verificar que estés en backend/
cd backend
pytest
```

---

## 📚 Documentación adicional

- **[SEGURIDAD_OWASP.md](SEGURIDAD_OWASP.md)** - Detalles de protecciones OWASP
- **[GITHUB_ACTIONS.md](GITHUB_ACTIONS.md)** - Guía de CI/CD
- **[TESTS_README.md](TESTS_README.md)** - Documentación de tests
- **[POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)** - Colección de Postman

---

## 🎓 Proyecto académico

Desarrollado como proyecto académico para demostrar:
- Arquitectura cliente-servidor
- API RESTful con autenticación JWT
- CRUD completo con control de acceso
- Seguridad según OWASP Top 10:2025
- Dockerización de aplicaciones
- Testing automatizado
- CI/CD con GitHub Actions

---

**🚀 ¡Listo para usar!** Accede a [http://localhost:8000/login.html](http://localhost:8000/login.html)