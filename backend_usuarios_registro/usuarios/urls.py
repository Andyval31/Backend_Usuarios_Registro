from django.urls import path
from .views import UsuarioListCreate

urlpatterns = [
    path('usuarios/', UsuarioListCreate.as_view()),
]
