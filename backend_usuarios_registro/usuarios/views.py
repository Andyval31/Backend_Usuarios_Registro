import json, requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from .models import Usuario

@csrf_exempt
def usuarios_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON inválido")

        nombre = data.get('nombre')
        email = data.get('email')

        if not nombre or not email:
            return HttpResponseBadRequest("Faltan campos obligatorios: nombre y email")

        try:
            usuario = Usuario.objects.create(nombre=nombre, email=email)
        except IntegrityError:
            return JsonResponse(
                {'error': f'El email {email} ya está registrado'},
                status=400
            )

        # Enviar notificación al microservicio Flask
        mensaje = {
            'mensaje': f"Usuario {usuario.nombre} creado correctamente",
            'email': usuario.email
        }
        try:
            requests.post('http://notificaciones:5000/notificaciones', json=mensaje, timeout=3)
        except Exception as e:
            print(f"Error al enviar notificación: {e}")

        return JsonResponse(
            {'mensaje': 'Usuario creado correctamente', 'id': usuario.id},
            status=201
        )

    elif request.method == 'GET':
        usuarios = list(Usuario.objects.values("id", "nombre", "email"))
        return JsonResponse(usuarios, safe=False)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
