from django.urls import path
from . import views

urlpatterns = [
    path("", views.registro, name="home"),  # página raíz abre registro
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"), 
    path('red_social/', views.red_social, name='red_social'),
    path("bienvenido/", views.bienvenido, name="bienvenido"),
    path("aviso/", views.aviso, name="aviso"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]
