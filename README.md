# 🚗 AppCoches

Aplicación web completa para la gestión y visualización de un catálogo de coches. Proyecto académico desarrollado con Python Flask (backend) y HTML/CSS/JavaScript (frontend), totalmente dockerizado.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#️-tecnologías)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
  - [Opción 1: Con Docker (Recomendado)](#opción-1-con-docker-recomendado)
  - [Opción 2: Sin Docker (Desarrollo Local)](#opción-2-sin-docker-desarrollo-local)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Base de Datos](#️-base-de-datos)
- [Funcionalidades](#-funcionalidades)
- [Solución de Problemas](#-solución-de-problemas)

---

## ✨ Características

- 🔐 **Sistema de autenticación** con JWT (JSON Web Tokens)
- 👤 **Dos roles de usuario**: Administrador y Usuario
- 🚗 **Gestión completa de coches** (CRUD) para administradores
- 🔍 **Filtros avanzados** de búsqueda (marca, modelo, año, precio)
- 📊 **Estadísticas** en tiempo real del catálogo
- 📸 **Subida y gestión de imágenes** para cada coche
- 🎨 **Interfaz responsive** y moderna
- 🐳 **Totalmente dockerizado** para fácil despliegue
- 💾 **Persistencia de datos** con MySQL

---

## 🛠️ Tecnologías

### Backend
- **Python 3.11**
- **Flask** - Framework web
- **MySQL** - Base de datos
- **JWT** - Autenticación con tokens
- **SHA-256** - Encriptación de contraseñas

### Frontend
- **HTML5**
- **CSS3** (con diseño moderno y gradientes)
- **JavaScript** (Vanilla JS)
- **Fetch API** - Comunicación con el backend

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación de contenedores

---

## 🏗️ Arquitectura

El proyecto utiliza una arquitectura de **microservicios con 2 contenedores**:

```
┌─────────────────────────────────────┐
│     Contenedor 1: Aplicación       │
│  ┌──────────────┐ ┌──────────────┐ │
│  │   Backend    │ │   Frontend   │ │
│  │  Flask:5000  │ │   HTTP:8000  │ │
│  └──────────────┘ └──────────────┘ │
└─────────────────────────────────────┘
                 ↕
┌─────────────────────────────────────┐
│     Contenedor 2: Base de Datos    │
│         MySQL 8.0 :3306            │
└─────────────────────────────────────┘
```

---

## 📦 Requisitos Previos

### Para Docker (Recomendado):
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado
- 4GB RAM mínimo
- Puertos libres: 3306, 5000, 8000

### Para desarrollo local:
- Python 3.11 o superior
- MySQL 8.0 o superior (XAMPP/WAMP)
- pip (gestor de paquetes de Python)

---

## 🚀 Instalación

### Opción 1: Con Docker (Recomendado)

#### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd appcoches
```

#### 2. Estructura de carpetas

Asegúrate de tener esta estructura:

```
appcoches/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── registro.py
│   ├── login.py
│   ├── coches.py
│   ├── requirements.txt
│   └── uploads/          (se crea automáticamente)
├── frontend/
│   ├── login.html
│   ├── registro.html
│   └── coches.html
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── start.sh
    ├── init.sql
    └── .dockerignore
```

#### 3. Detener servicios locales

Si tienes XAMPP o WAMP corriendo, **deténlos** para liberar los puertos.

#### 4. Levantar los contenedores

Desde la carpeta `docker/`:

```bash
cd docker
docker-compose up -d
```

#### 5. Verificar que está corriendo

```bash
docker-compose ps
```

Deberías ver:

```
NAME                STATUS              PORTS
appcoches-mysql     Up                  0.0.0.0:3306->3306/tcp
appcoches-app       Up                  0.0.0.0:5000->5000/tcp, 0.0.0.0:8000->8000/tcp
```

#### 6. Acceder a la aplicación

Abre tu navegador y ve a:

```
http://localhost:8000/login.html
```

---

### Opción 2: Sin Docker (Desarrollo Local)

#### 1. Instalar dependencias

Desde la carpeta `backend/`:

```bash
cd backend
python -m pip install -r requirements.txt
```

#### 2. Configurar MySQL

- Inicia XAMPP o WAMP
- Abre phpMyAdmin: `http://localhost/phpmyadmin`
- Ejecuta el script SQL que está en `docker/init.sql`

#### 3. Actualizar configuración

Edita `backend/config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_contraseña',  # Tu contraseña de MySQL
    'database': 'appcoches',
    'charset': 'utf8mb4'
}
```

#### 4. Iniciar backend

```bash
cd backend
python app.py
```

#### 5. Iniciar frontend

En otra terminal:

```bash
cd frontend
python -m http.server 8000
```

#### 6. Acceder a la aplicación

```
http://localhost:8000/login.html
```

---

## 💻 Uso

### Credenciales por defecto

#### Administrador:
```
Email: admin@ejemplo.com
Password: admin123
```


### Flujo de uso

1. **Login**: Inicia sesión con las credenciales
2. **Visualización**: Todos los usuarios pueden ver el catálogo de coches
3. **Filtros**: Usa los filtros para buscar coches específicos
4. **Administración** (solo admin):
   - Añadir nuevos coches con imagen
   - Editar coches existentes
   - Eliminar coches del catálogo

---

## 📁 Estructura del Proyecto

```
appcoches/
│
├── backend/                    # Backend Flask
│   ├── app.py                 # Aplicación principal
│   ├── config.py              # Configuración (BD, JWT)
│   ├── database.py            # Gestión de conexión MySQL
│   ├── registro.py            # Endpoint de registro
│   ├── login.py               # Endpoint de login y JWT
│   ├── coches.py              # CRUD de coches
│   ├── requirements.txt       # Dependencias Python
│   └── uploads/               # Imágenes de coches
│       └── coches/
│
├── frontend/                   # Frontend HTML/CSS/JS
│   ├── login.html             # Página de inicio de sesión
│   ├── registro.html          # Página de registro
│   └── coches.html            # Página principal (catálogo)
│
└── docker/                     # Configuración Docker
    ├── Dockerfile             # Imagen de la aplicación
    ├── docker-compose.yml     # Orquestación
    ├── start.sh               # Script de inicio
    ├── init.sql               # Script de BD inicial
    └── .dockerignore          # Archivos a ignorar
```

---

## 🌐 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/registro` | Registrar nuevo usuario | No |
| POST | `/api/login` | Iniciar sesión (devuelve JWT) | No |
| GET | `/api/verificar-token` | Verificar validez del token | Sí |

### Coches

| Método | Endpoint | Descripción | Auth | Admin |
|--------|----------|-------------|------|-------|
| GET | `/api/coches` | Listar todos los coches (con filtros) | No | No |
| GET | `/api/coches/:id` | Obtener un coche específico | No | No |
| POST | `/api/coches` | Crear nuevo coche | Sí | Sí |
| PUT | `/api/coches/:id` | Editar coche existente | Sí | Sí |
| DELETE | `/api/coches/:id` | Eliminar coche | Sí | Sí |
| GET | `/api/marcas` | Listar marcas disponibles | No | No |
| GET | `/api/estadisticas` | Obtener estadísticas del catálogo | No | No |
| GET | `/api/uploads/:filename` | Obtener imagen de coche | No | No |

### Filtros disponibles (GET /api/coches)

- `marca`: Filtrar por marca (búsqueda parcial)
- `modelo`: Filtrar por modelo (búsqueda parcial)
- `año_min`: Año mínimo
- `año_max`: Año máximo
- `precio_min`: Precio mínimo
- `precio_max`: Precio máximo
- `ordenar`: Campo de ordenación (marca, modelo, año, precio)
- `orden`: Dirección (ASC o DESC)

**Ejemplo:**
```
GET /api/coches?marca=BMW&precio_max=30000&ordenar=precio&orden=ASC
```

---

## 🗄️ Base de Datos

### Tabla: `usuarios`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | ID único (auto-increment) |
| nombre | VARCHAR(100) | Nombre completo |
| email | VARCHAR(100) | Email único |
| password | VARCHAR(255) | Contraseña encriptada (SHA-256) |
| rol | ENUM('admin','usuario') | Rol del usuario |
| fecha_registro | TIMESTAMP | Fecha de creación |

### Tabla: `coches`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | ID único (auto-increment) |
| marca | VARCHAR(50) | Marca del coche |
| modelo | VARCHAR(50) | Modelo del coche |
| año | INT | Año de fabricación |
| precio | DECIMAL(10,2) | Precio en euros |
| descripcion | TEXT | Descripción detallada |
| imagen | VARCHAR(255) | Nombre del archivo de imagen |

---

## 🎯 Funcionalidades

### Para todos los usuarios:
- ✅ Ver catálogo completo de coches
- ✅ Filtrar por marca, modelo, año y precio
- ✅ Ordenar resultados
- ✅ Ver detalles de cada coche
- ✅ Ver estadísticas del catálogo
- ✅ Registrarse en el sistema
- ✅ Iniciar sesión

### Para administradores:
- ✅ Todas las funcionalidades de usuario
- ✅ Añadir nuevos coches con imagen
- ✅ Editar información de coches
- ✅ Cambiar imagen de un coche
- ✅ Eliminar coches del catálogo
- ✅ Badge visual "ADMIN" en la interfaz

---

## 🐳 Comandos Docker

### Iniciar la aplicación
```bash
docker-compose up -d
```

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Ver logs de un contenedor específico
```bash
docker-compose logs -f app    # Backend + Frontend
docker-compose logs -f db     # MySQL
```

### Ver estado de los contenedores
```bash
docker-compose ps
```

### Detener la aplicación
```bash
docker-compose down
```

### Detener y eliminar volúmenes (¡borra la BD!)
```bash
docker-compose down -v
```

### Reiniciar la aplicación
```bash
docker-compose restart
```

### Reconstruir las imágenes
```bash
docker-compose up --build
```

### Acceder al contenedor de la aplicación
```bash
docker exec -it appcoches-app bash
```

### Acceder a MySQL desde línea de comandos
```bash
docker exec -it appcoches-mysql mysql -u root -pAppCoches9393 appcoches
```

---

## 🔧 Solución de Problemas

### Puerto ocupado

**Problema:** `Error: port is already allocated`

**Solución:**
- Detén XAMPP/WAMP si está corriendo
- Verifica puertos en uso:
  ```bash
  # Windows
  netstat -ano | findstr :3306
  netstat -ano | findstr :5000
  netstat -ano | findstr :8000
  ```

### Error de conexión a MySQL

**Problema:** `Can't connect to MySQL server`

**Solución:**
- Espera unos segundos, MySQL tarda en inicializarse
- Verifica logs: `docker-compose logs db`
- Reinicia: `docker-compose restart db`

### Los cambios no se reflejan

**Problema:** Edité el código pero no veo los cambios

**Solución:**
```bash
docker-compose down
docker-compose up --build
```

### Error al subir imágenes

**Problema:** Las imágenes no se suben o no se ven

**Solución:**
- Verifica que la carpeta `backend/uploads/coches/` exista
- Verifica permisos de escritura
- Tamaño máximo: 5MB por imagen
- Formatos soportados: JPG, PNG, GIF, WEBP

### Contenedor no inicia

**Problema:** `Container exited with code 1`

**Solución:**
```bash
# Ver logs detallados
docker-compose logs app

# Verificar que todos los archivos estén en su lugar
ls -la backend/
ls -la frontend/
ls -la docker/
```

### Olvidé mi contraseña

**Problema:** No puedo iniciar sesión

**Solución:**
```bash
# Acceder a MySQL
docker exec -it appcoches-mysql mysql -u root -pAppCoches9393 appcoches

# Actualizar contraseña (desde MySQL)
UPDATE usuarios SET password = SHA2('nueva_contraseña', 256) WHERE email = 'tu@email.com';
exit;
```

---

## 📊 Datos de Ejemplo

La aplicación viene pre-cargada con:

- **2 usuarios**: 1 administrador y 1 usuario normal
- **12 coches** de diferentes marcas:
  - Audi S5 Coupé (2012) - 26.000€
  - BMW 335i Coupé (2007) - 17.000€
  - BMW M5 E60 (2006) - 30.000€
  - Volvo XC60 B4 (2023) - 40.000€
  - Volkswagen Scirocco R (2009) - 13.500€
  - Volkswagen Golf R32 (2008) - 15.000€
  - Audi S8 D3 (2006) - 23.000€
  - Seat Arona (2024) - 26.000€
  - Opel Corsa (2021) - 10.500€
  - Mercedes-Benz CLS 400 (2016) - 27.600€
  - BMW X6 (2014) - 26.000€
  - Seat Ibiza (2018) - 12.100€

---

## 🔒 Seguridad

- Contraseñas encriptadas con **SHA-256**
- Autenticación mediante **JWT** con expiración de 24 horas
- Validación de roles en el backend
- CORS configurado para desarrollo
- Subida de archivos con validación de tipo y tamaño
- Prevención de SQL injection con queries parametrizadas

