from django.urls import path
from . import views

urlpatterns = [
    path("", views.registro, name="home"),  # página raíz abre registro
    path("registro/", views.registro, name="registro"),
    path("bienvenido/", views.bienvenido, name="bienvenido"),
    path("aviso/", views.aviso, name="aviso"),
]
