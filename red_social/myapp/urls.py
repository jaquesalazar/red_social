from django.urls import path
from . import views

urlpatterns = [
    path("", views.registro, name="home"),  # página raíz abre registro
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"), 
    path('red_social/', views.red_social, name='red_social'),
    path('nueva_publicacion/', views.nueva_publicacion, name='nueva_publicacion'),
    path("bienvenido/", views.bienvenido, name="bienvenido"),
    path("aviso/", views.aviso, name="aviso"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('like/<str:post_id>/', views.dar_like, name='dar_like'),
    path('comentar/<str:post_id>/', views.comentar_publicacion, name='comentar_publicacion'),
    path('eliminar/<str:post_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
]
