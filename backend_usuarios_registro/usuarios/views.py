from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Usuario
from .serializers import UsuarioSerializer
import requests

@method_decorator(csrf_exempt, name='dispatch')
class UsuarioListCreate(APIView):
    
    def finalize_response(self, request, response, *args, **kwargs):
        """Agregar headers CORS a todas las respuestas"""
        response = super().finalize_response(request, response, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response['Access-Control-Max-Age'] = '86400'
        return response
    
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()

            # Notificación
            try:
                mensaje = {
                    "email": usuario.email,
                    "mensaje": f"Usuario {usuario.nombre} creado correctamente"
                }
                requests.post("http://notificaciones:5000/notify", json=mensaje)
            except Exception as e:
                print(f"Error al enviar notificación: {e}")

            return Response({"mensaje": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def options(self, request, *args, **kwargs):
        """Manejar peticiones OPTIONS para CORS preflight"""
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response['Access-Control-Max-Age'] = '86400'
        response.status_code = 200
        return response