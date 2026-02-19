#!/bin/bash

# Script para iniciar backend y frontend simultáneamente

# Esperar a que MySQL esté listo
echo "Esperando a que MySQL esté disponible..."
while ! nc -z db 3306; do
  sleep 1
done
echo "MySQL está listo!"

# Iniciar el backend Flask en segundo plano
echo "Iniciando backend Flask en puerto 5000..."
python app.py &

# Esperar un momento para que Flask se inicie
sleep 3

# Iniciar el servidor HTTP para el frontend en la carpeta frontend
echo "Iniciando servidor frontend en puerto 8000..."
cd /app/frontend
python -m http.server 8000

# Mantener el contenedor activo
wait