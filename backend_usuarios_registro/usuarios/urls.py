from django.urls import path
from .views import UsuarioListCreate

urlpatterns = [
    path('', UsuarioListCreate.as_view()),
]
