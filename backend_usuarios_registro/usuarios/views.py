from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
import requests

class UsuarioListCreate(APIView):
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
