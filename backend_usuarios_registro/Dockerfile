FROM python:3.11

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto
EXPOSE 5000

# Comando para correr Django con Gunicorn con timeout aumentado
CMD ["gunicorn", "backend_usuarios_registro.wsgi:application", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "2"]