# Dockerfile para la aplicación (Backend Flask + Frontend)
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema y netcat para healthcheck
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements desde la carpeta backend
COPY backend/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos del backend
COPY backend/*.py ./

# Copiar archivos del frontend
COPY frontend/ ./frontend/

# Crear directorio para imágenes
RUN mkdir -p uploads/coches

# Exponer puertos
# 5000 para el backend Flask
# 8000 para el servidor HTTP del frontend
EXPOSE 5000 8000

# Copiar script de inicio (desde la carpeta docker dentro del contexto)
COPY docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Ejecutar el script de inicio
CMD ["/app/start.sh"]