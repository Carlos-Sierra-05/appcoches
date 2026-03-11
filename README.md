# 🚗 AppCoches

Aplicación web full-stack para la gestión de un catálogo de coches con autenticación JWT, control de acceso basado en roles y protección completa contra OWASP Top 10:2025.

[![CI/CD](https://img.shields.io/badge/CI/CD-passing-brightgreen)](https://github.com)
[![Security](https://img.shields.io/badge/OWASP-Top%2010%20Protected-blue)](https://owasp.org)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-73%20passing-brightgreen)](https://pytest.org)

---

## 📸 Imagen de la APP

<img width="993" height="865" alt="Admin" src="https://github.com/user-attachments/assets/f910d3d8-eb8d-49e5-b458-381e1647378d" />

---

## 📋 Características

- 🔐 **Autenticación JWT** con bcrypt (12 rondas) y expiración de 2h
- 👥 **Control de acceso (RBAC)** - Admin y Usuario
- 🚗 **CRUD completo** con gestión de imágenes
- 🔍 **Filtros avanzados** por marca, modelo, año, precio
- 🛡️ **OWASP Top 10:2025** - 10/10 protegido
- 🐳 **Dockerizado** - 2 contenedores (MySQL + App)
- 🧪 **73 tests** automatizados con pytest
- 📝 **Logging** completo de seguridad
- ⚡ **Rate limiting** y bloqueo de cuenta (5 intentos)

---

## 🛠️ Stack

**Backend:** Python 3.11, Flask, MySQL 8.0, JWT, bcrypt, Flask-Limiter  
**Frontend:** HTML5, CSS3, JavaScript  
**Testing:** Pytest (82 tests), pytest-cov  
**DevOps:** Docker, GitHub Actions, Flake8, Bandit

---

## 🚀 Inicio rápido

### Con Docker (Recomendado)
```bash
git clone <url-repositorio> && cd appcoches
cd docker && docker-compose up -d
# Frontend: http://localhost:8000/login.html
```

### Sin Docker
```bash
cd backend && pip install -r requirements.txt
# Ejecutar docker/init.sql en MySQL
python app.py
# En otra terminal: cd frontend && python -m http.server 8000
```

**Credenciales admin:** `admin@ejemplo.com` / `admin123`

---

## 📁 Estructura

```
appcoches/
├── .github/workflows/ci-cd.yml    # CI/CD
├── backend/
│   ├── tests/                     # 82 tests (pytest)
│   ├── logs/                      # Logs de seguridad
│   ├── uploads/                   # Imágenes
│   ├── app.py, config.py
│   ├── login.py, registro.py
│   ├── coches.py                  # CRUD
│   ├── security_logger.py
│   └── requirements.txt
├── frontend/
│   ├── login.html, registro.html
│   └── coches.html
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── init.sql                   # BD con datos
├── Imagenes App/                  # Screenshots
├── APP-COCHES.postman_collection.json
├── README.md
└── bbdd.sql
```

---

## 🌐 API Endpoints

**Públicos (sin auth):**
```
GET  /api/coches              # Listar (con filtros)
GET  /api/coches/:id          # Obtener uno
GET  /api/marcas              # Lista marcas
GET  /api/estadisticas        # Estadísticas
POST /api/registro            # Registrar usuario
POST /api/login               # Login (devuelve JWT)
```

**Protegidos (admin + JWT):**
```
POST   /api/coches            # Crear
PUT    /api/coches/:id        # Editar
DELETE /api/coches/:id        # Eliminar
```

**Filtros:** `?marca=BMW&precio_min=20000&ordenar=precio&orden=DESC`

---

## 🧪 Tests - 73 automatizados

**Ejecutar:**
```bash
cd backend
pytest                    # Todos
pytest -m auth           # Solo autenticación
pytest -m security       # Solo seguridad
pytest --cov=.           # Con cobertura
```
<img width="1362" height="376" alt="cap pruebas pytest" src="https://github.com/user-attachments/assets/01781e4a-c037-4b1c-a6f5-acf6813f89f7" />

---
## 📬 Postman

Archivo: APP-COCHES.postman_collection.json

La colección de Postman incluye pruebas automáticas para los endpoints principales de la API.

**1️⃣ Autenticación**

POST /api/registro

Registra un nuevo usuario y valida el formato del email y la contraseña.

<img width="1381" height="228" alt="CAP REGISTRO" src="https://github.com/user-attachments/assets/53a2feb5-a033-4b81-96a4-6fdc69b03083" />

POST /api/login

Inicia sesión y guarda automáticamente el token JWT en la variable {{auth_token}}.

<img width="1383" height="391" alt="CAP LOGIN" src="https://github.com/user-attachments/assets/dea936c3-ba1c-4464-9e6e-37735a47dad1" />

**2️⃣ Consultas públicas**

GET /api/coches

Obtiene los coches filtrando por precio mínimo (> 20000€) y ordenados por precio descendente.

<img width="1377" height="418" alt="CAP GET" src="https://github.com/user-attachments/assets/f757a095-0670-49c3-9c10-f5f433010c93" />

Tests incluidos:

-Verifica status 200

-Comprueba que la respuesta es JSON

-Valida la estructura de datos

-Verifica que todos los coches cuestan más de 20.000€

-Comprueba que están ordenados por precio

-Verifica que cada coche tiene id, marca, modelo, año y precio

**3️⃣ CRUD de coches (Solo Admin)**

Requiere autenticación con token JWT.

POST /api/coches

Crea un coche nuevo y guarda automáticamente {{ultimo_coche_id}}.

<img width="1382" height="223" alt="CAP CREAR" src="https://github.com/user-attachments/assets/6472b31b-42c7-43ac-ad5f-8b01c84eb142" />

PUT /api/coches/:id

Edita un coche existente.

<img width="1386" height="213" alt="CAP EDITAR" src="https://github.com/user-attachments/assets/38a87744-7ab7-4ee5-a8f8-bedc33fad592" />

DELETE /api/coches/:id

Elimina un coche.

<img width="1391" height="208" alt="CAP eliminar" src="https://github.com/user-attachments/assets/dc14d595-7faf-4035-9688-1bd3c7f9d533" />

📥 Importar colección

Abrir Postman

Click en Import

Arrastrar el archivo:

APP-COCHES.postman_collection.json

---

## 🛡️ OWASP Top 10:2025

| # | Vulnerabilidad | Protección |
|---|----------------|------------|
| **A01** | Broken Access Control | Decoradores `@requiere_admin`, logs de auditoría |
| **A02** | Security Misconfiguration | Headers (HSTS, CSP, XSS), CORS configurado, debug=false |
| **A03** | Supply Chain | Versiones fijas (Flask==3.0.0, bcrypt==4.1.2) |
| **A04** | Cryptographic Failures | bcrypt 12 rondas, JWT con expiración 2h, SECRET_KEY aleatoria |
| **A05** | Injection | Queries parametrizadas, validación entrada, `secure_filename()` |
| **A06** | Insecure Design | Rate limit (5 login/min), validaciones de negocio |
| **A07** | Authentication Failures | Bloqueo 5 intentos = 15min, contraseñas robustas (8+ chars, mayús, núm) |
| **A08** | Data Integrity | Validación MIME, límite 5MB, whitelist extensiones |
| **A09** | Logging Failures | 12 eventos logueados (login, admin actions, errors), rotación 10MB |
| **A10** | Exception Handling | Manejadores específicos 400/401/403/404/500, mensajes genéricos |

**Ejemplos de protecciones:**

```python
# A04 - bcrypt
salt = bcrypt.gensalt(rounds=12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

# A07 - Bloqueo de cuenta
if failed_attempts[email]['count'] >= 5:
    locked_accounts[email] = time.time()
    return "Bloqueada 15 min", 429

# A09 - Logging
log_login_failure(email, ip, "Usuario no existe", user_agent)
```

**Eventos logueados:** LOGIN_SUCCESS, LOGIN_FAILURE, ACCOUNT_LOCKED, REGISTER, UNAUTHORIZED_ACCESS, TOKEN_EXPIRED, ADMIN_ACTION, RATE_LIMIT, FILE_UPLOAD, ERRORS

---

## 🐳 Docker

**2 contenedores:**
- **MySQL 8.0** (puerto 3306) - BD persistente + init.sql
- **App** (puertos 5000 + 8000) - Flask backend + Frontend

```bash
docker-compose up -d          # Iniciar
docker-compose logs -f        # Ver logs
docker-compose ps             # Estado
docker-compose down           # Detener
docker-compose restart        # Reiniciar
```
<img width="1626" height="188" alt="image" src="https://github.com/user-attachments/assets/298357cd-dbfe-4844-a504-c4866024bdc7" />

---

## 📊 Base de datos

**Tablas:**
- `usuarios` (id, nombre, email, password_bcrypt, rol, fecha)
- `coches` (id, marca, modelo, año, precio, descripcion, imagen)

**Datos iniciales:**
- 2 usuarios (1 admin, 1 usuario)
- 12 coches (Audi, BMW, Mercedes, Volvo, VW, Seat, Opel)
  
<img width="547" height="255" alt="cap bbdd" src="https://github.com/user-attachments/assets/8dc68eb8-3e1e-4919-b855-1d3720ad0e9d" />

---

## 🔄 CI/CD GitHub Actions

**GitHub Actions** (`.github/workflows/ci-cd.yml`):
1. Validar sintaxis Python (flake8)
2. Ejecutar 73 tests (pytest + MySQL)
3. Validar estructura proyecto
4. Escaneo seguridad (Safety + Bandit)

**Triggers:** Push a main/master/develop, Pull Requests
<img width="1445" height="282" alt="image" src="https://github.com/user-attachments/assets/2f789b4c-f9c2-4bf6-8c29-aa2ed8a31efd" />

---

## 🎓 Proyecto académico

Demuestra:
✅ API RESTful con JWT  
✅ Seguridad OWASP Top 10:2025 (10/10)  
✅ Testing (73 tests)  
✅ Dockerización  
✅ CI/CD  
✅ RBAC (roles)  
✅ Logging/auditoría  

---

## 🔐 Features de seguridad

- **Contraseñas:** bcrypt 12 rondas
- **Tokens:** JWT 2h expiración
- **Rate limit:** 5 login/min, 100 API/min
- **Bloqueo:** 5 fallos = 15min
- **Headers:** HSTS, CSP, X-Frame-Options, X-XSS-Protection
- **Logs:** 12 tipos eventos en `logs/security.log`
- **Validaciones:** Email, contraseñas (8+ chars, mayús, núm), archivos (5MB, tipos)
- **SQL:** Queries parametrizadas

---

**🚀 Acceso:** [http://localhost:8000/login.html](http://localhost:8000/login.html)

**📧 Admin:** admin@ejemplo.com / admin123
