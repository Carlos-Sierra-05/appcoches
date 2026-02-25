# 🛡️ Protección OWASP Top 10:2025 - AppCoches

## 📊 Estado de Seguridad del Proyecto

Este documento detalla las protecciones implementadas en AppCoches frente a las vulnerabilidades de OWASP Top 10:2025.

---

## 🔐 **DETALLES POR VULNERABILIDAD**

### **A01:2025 - Broken Access Control** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Protecciones implementadas:**
- ✅ Decoradores de autenticación (`@verificar_token`, `@requiere_admin`)
- ✅ Verificación de roles en endpoints sensibles
- ✅ Validación de permisos a nivel de función
- ✅ Separación clara entre endpoints públicos y protegidos
- ✅ Validación de IDs y recursos solicitados
- ✅ Mensajes de error apropiados (401, 403, 404)

**Endpoints protegidos:**
```
POST   /api/coches          → Solo admin (crear)
PUT    /api/coches/:id      → Solo admin (editar)
DELETE /api/coches/:id      → Solo admin (eliminar)
```

**Endpoints públicos:**
```
GET /api/coches              → Todos (listar)
GET /api/coches/:id          → Todos (ver detalle)
GET /api/marcas              → Todos (marcas)
GET /api/estadisticas        → Todos (stats)
```

**Código implementado:**
```python
@requiere_admin
def crear_coche():
    # Verifica token JWT válido
    # Verifica rol == 'admin'
    # Solo entonces permite acceso
```

---

### **A02:2025 - Security Misconfiguration** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Configuraciones seguras implementadas:**
- ✅ Debug mode controlado por variable de entorno
- ✅ SECRET_KEY generada aleatoriamente (no hardcodeada)
- ✅ CORS configurado solo para orígenes permitidos
- ✅ Headers de seguridad implementados
- ✅ Variables sensibles en configuración externa
- ✅ Información del servidor oculta

**Headers de seguridad activos:**
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

**Configuración de CORS:**
```python
ALLOWED_ORIGINS = ['http://localhost:8000', 'http://localhost:3000']
# Solo estos orígenes pueden hacer peticiones
```

---

### **A03:2025 - Software Supply Chain Failures** ✅

**Estado:** PROTEGIDO

**Medidas implementadas:**
- ✅ Versiones exactas de todas las dependencias
- ✅ Dependencias mínimas necesarias
- ✅ Paquetes verificados y actualizados

**Dependencias con versiones fijas:**
```
Flask==3.0.0
flask-cors==4.0.0
mysql-connector-python==8.2.0
PyJWT==2.8.0
bcrypt==4.1.2
Flask-Limiter==3.5.0
email-validator==2.1.0
```

---

### **A04:2025 - Cryptographic Failures** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Mejoras implementadas:**
- ✅ **bcrypt** para hashing de contraseñas (reemplaza SHA-256)
- ✅ Salt automático con 12 rondas
- ✅ SECRET_KEY aleatoria y robusta
- ✅ Tokens JWT con expiración reducida (2 horas)
- ✅ Migración automática de contraseñas antiguas

**Antes (INSEGURO):**
```python
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

**Ahora (SEGURO):**
```python
salt = bcrypt.gensalt(rounds=12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
# Computacionalmente costoso de crackear
```

**Características de bcrypt:**
- Algoritmo adaptativo (ajustable en el futuro)
- Resistente a ataques de fuerza bruta
- Salt único por contraseña
- Estándar de la industria

---

### **A05:2025 - Injection** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Protecciones contra SQL Injection:**
- ✅ Queries parametrizadas en TODAS las consultas
- ✅ Whitelist de campos de ordenamiento
- ✅ Validación estricta de entrada
- ✅ `secure_filename()` para nombres de archivo

**Ejemplo de código seguro:**
```python
# Parametrizado (SEGURO)
query = "SELECT * FROM coches WHERE marca = %s"
execute_query(query, (marca,), fetch=True)

# NO concatenación (INSEGURO - NO usado)
# query = f"SELECT * FROM coches WHERE marca = '{marca}'"
```

**Protección contra Path Traversal:**
```python
filename = secure_filename(filename)
# Previene ../../../etc/passwd
```

---

### **A06:2025 - Insecure Design** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Diseños de seguridad implementados:**
- ✅ Rate limiting global y por endpoint
- ✅ Validaciones robustas de entrada
- ✅ Límites de tamaño de archivo (5MB)
- ✅ Validaciones de rangos (año: 1900-2030, precio: 0-1M)
- ✅ Tokens JWT con expiración corta (2h)
- ✅ Separación de roles clara

**Rate Limits configurados:**
```
Login:    5 intentos por minuto
Registro: 3 intentos por hora
API:      100 peticiones por minuto
```

**Validaciones de negocio:**
```python
# Año válido
if año < 1900 or año > 2030:
    return error

# Precio razonable
if precio < 0 or precio > 1000000:
    return error

# Tamaño de imagen
if len(imagen_data) > 5MB:
    return error
```

---

### **A07:2025 - Authentication Failures** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Protecciones de autenticación:**
- ✅ **Bloqueo de cuenta** tras 5 intentos fallidos
- ✅ Lockout de 15 minutos
- ✅ **Contraseñas robustas obligatorias:**
  - Mínimo 8 caracteres
  - Al menos 1 mayúscula
  - Al menos 1 minúscula
  - Al menos 1 número
- ✅ Tokens JWT con expiración de 2 horas
- ✅ Rate limiting en endpoints de autenticación
- ✅ Validación de formato de email
- ✅ Mensajes genéricos de error (no revelar si email existe)

**Mecanismo de bloqueo:**
```python
MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutos

# Tras 5 intentos fallidos:
if failed_attempts >= 5:
    locked_accounts[email] = timestamp
    return "Cuenta bloqueada 15 minutos", 429
```

**Validación de contraseñas:**
```python
def validar_contraseña(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True
```

---

### **A08:2025 - Software or Data Integrity Failures** ✅

**Estado:** PROTEGIDO

**Protecciones de integridad:**
- ✅ Validación de tipos de archivo (png, jpg, jpeg, gif, webp)
- ✅ Límite de tamaño de archivo (5MB)
- ✅ Sanitización de nombres con `secure_filename()`
- ✅ Validación de datos de entrada
- ✅ Verificación de tipos de datos

**Validación de subida de archivos:**
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

---

### **A09:2025 - Security Logging and Alerting Failures** ⚠️

**Estado:** PROTECCIÓN BÁSICA

**Logging actual:**
- ⚠️ Prints básicos en consola
- ⚠️ Sin archivos de log estructurados
- ⚠️ Sin sistema de alertas

**Lo que SÍ se registra (mediante prints):**
- Errores de conexión a BD
- Excepciones en endpoints
- Errores al procesar archivos

**Recomendación para el futuro:**
- Implementar logging estructurado con el módulo `logging`
- Guardar logs en archivos con rotación
- Monitoreo de eventos de seguridad
- Alertas para actividad sospechosa

**Nota:** Esta es la única vulnerabilidad con protección básica en lugar de completa.

---

### **A10:2025 - Mishandling of Exceptional Conditions** ✅

**Estado:** COMPLETAMENTE PROTEGIDO

**Manejo de excepciones implementado:**
- ✅ Manejadores específicos para cada código HTTP
- ✅ Try-catch en todos los endpoints críticos
- ✅ Mensajes de error genéricos (no exponen detalles internos)
- ✅ Validación de entrada antes de procesamiento

**Errores manejados:**
```
400 - Bad Request
401 - Unauthorized
403 - Forbidden
404 - Not Found
405 - Method Not Allowed
429 - Too Many Requests
500 - Internal Server Error
```

**Ejemplo de manejo:**
```python
@app.errorhandler(500)
def internal_error(error):
    # NO expone detalles del error al usuario
    return jsonify({
        'success': False,
        'message': 'Error interno del servidor'
    }), 500
```

## 🎯 **CARACTERÍSTICAS DE SEGURIDAD DESTACADAS**

### **Autenticación Robusta:**
```
✅ JWT con expiración de 2 horas
✅ bcrypt con 12 rondas de salt
✅ Bloqueo tras 5 intentos fallidos
✅ Lockout de 15 minutos
✅ Contraseñas robustas obligatorias (8+ chars, mayús, minús, número)
✅ Rate limiting (5 login/min, 3 registro/hora)
```

### **Control de Acceso:**
```
✅ Decoradores de autorización
✅ Verificación de roles (admin/usuario)
✅ Validación de permisos por endpoint
✅ Separación clara de endpoints públicos/privados
```

### **Protección de Datos:**
```
✅ Queries parametrizadas (anti SQL injection)
✅ Validación estricta de entrada
✅ Sanitización de nombres de archivo
✅ Límites de tamaño y tipo de archivo
```

### **Configuración Segura:**
```
✅ Headers de seguridad (HSTS, CSP, X-Frame-Options, etc.)
✅ CORS restringido a orígenes permitidos
✅ Debug mode controlado
✅ SECRET_KEY aleatoria
```

### **Criptografía:**
```
✅ bcrypt para contraseñas (estándar de la industria)
✅ JWT para sesiones
✅ Salt automático por contraseña
✅ 12 rondas de hashing
```

