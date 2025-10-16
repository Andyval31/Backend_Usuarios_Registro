# Imagen base con Python
FROM python:3.11-slim

# Instalar netcat para esperar la base
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . /app

# Dar permisos al script
RUN chmod +x /app/espera_por_bd.sh

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa Flask
EXPOSE 5000


# Usar el script como punto de entrada
CMD ["/app/espera_por_bd.sh"]
