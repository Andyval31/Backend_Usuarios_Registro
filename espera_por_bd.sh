#!/bin/bash
echo "Esperando a que PostgreSQL esté disponible..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL está listo. Iniciando Flask..."
exec python app.py
