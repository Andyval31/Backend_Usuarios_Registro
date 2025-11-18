# Users API Service - Backend

## Descripción

API REST desarrollada en Django/Python para gestión de usuarios. Permite crear y consultar usuarios, comunicándose con el servicio de notificaciones para enviar alertas por email.

## Tecnologías

- Python 3.9+
- Django 4.2+
- Django REST Framework
- PostgreSQL 13+
- Docker & Docker Compose

## Estructura del Proyecto

```
backend_usuarios_registro/
├── users_api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services.py
├── backend_usuarios_registro/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── README.md
```

## Dependencias

```txt
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.9
python-decouple==3.8
requests==2.31.0
django-cors-headers==4.3.1
gunicorn==21.2.0
```

## Instalación Local

### 1. Crear red Docker

```bash
docker network create app-network
docker network ls | grep app-network
```

### 2. Clonar y configurar en rama despliegue-aws

```bash
git clone https://github.com/Andyval31/Backend_Usuarios_Registro.git Backend_Usuarios_Registro
cd Backend_Usuarios_Registro/backend_usuarios_registro
cp .env.example .env
nano .env  # Configurar variables
```

### 3. Configurar .env

```env
# Base de datos
DB_ENGINE=django.db.backends.postgresql
DB_HOST=db
DB_PORT=5432
DB_NAME=usuarios_db
DB_USER=postgres
DB_PASSWORD=postgres123

# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend-usuarios

# Notificaciones (Ejercicio 2)
NOTIFICATION_SERVICE_URL=http://notification-service:8002

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 4. Levantar servicios

```bash
docker-compose up -d
sleep 15
docker exec -it backend-usuarios python3 manage.py migrate
docker exec -it backend-usuarios python3 manage.py createsuperuser
```

### 5. Verificar

```bash
docker ps | grep backend
docker logs -f backend-usuarios
# Acceder a http://localhost:8000/api/
```

## Endpoints API

### Crear Usuario

```http
POST /api/users/
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "telefono": "+598 99 123 456"
}
```

**Respuesta (201)**:
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "telefono": "+598 99 123 456",
  "created_at": "2025-11-18T10:30:00Z"
}
```

### Listar Usuarios

```http
GET /api/users/
```

**Respuesta (200)**:
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "telefono": "+598 99 123 456",
    "created_at": "2025-11-18T10:30:00Z"
  }
]
```

### Obtener Usuario

```http
GET /api/users/{id}/
```

## Comandos Útiles

```bash
# Ver logs
docker logs -f backend-usuarios

# Shell Django
docker exec -it backend-usuarios python3 manage.py shell

# Crear migraciones
docker exec -it backend-usuarios python3 manage.py makemigrations
docker exec -it backend-usuarios python3 manage.py migrate

# Tests
docker exec -it backend-usuarios python3 manage.py test

# Detener
docker-compose down

# Detener y borrar BD
docker-compose down -v
```

## Despliegue en AWS EKS

### 1. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend_usuarios_registro.wsgi:application"]
```

### 2. Build y Push a ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t users-api-service .
docker tag users-api-service:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/users-api-service:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/users-api-service:latest
```

### 3. Manifiestos Kubernetes

Ver carpeta `k8s/`:
- `deployment.yaml` - Configuración del deployment
- `service.yaml` - Service ClusterIP
- `configmap.yaml` - Variables de configuración
- `secret.yaml` - Credenciales

## Seguridad

### Análisis SAST

```bash
pip install bandit pylint
bandit -r .
pylint users_api/
```

### Análisis SCA

```bash
pip install safety
safety check
```

### Escaneo de Imagen

```bash
trivy image users-api-service:latest
```

## Troubleshooting

### Error: Connection refused a BD

```bash
# Verificar que PostgreSQL esté corriendo
docker ps | grep postgres
docker logs postgres-db

# Reiniciar
docker-compose down -v
docker-compose up -d
sleep 15
docker exec -it backend-usuarios python3 manage.py migrate
```

### Error: Notification service unavailable

```bash
# Verificar que notification-service esté corriendo
docker ps | grep notification

# Verificar red
docker network inspect app-network
```

## Repositorios Relacionados
# Rama despliegue-aws
- Frontend: `https://github.com/Andyval31/Frontend_Usuarios_Registro.git`
- Notificaciones: `https://github.com/Andyval31/Notificaciones.git`

---

**UTEC - Administración de Infraestructuras - 2025**
**Integrantes: Matias Ferreira y Andrea Valdez**