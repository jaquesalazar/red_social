from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from .forms import RegistroForm
from mongo import users_coll, posts_coll  # Usa tus colecciones existentes
from bson import ObjectId


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = make_password(form.cleaned_data["password"])
            consent = form.cleaned_data["consent"]

            if users_coll.find_one({"email": email}):
                form.add_error("email", "Este correo ya está registrado.")
            else:
                users_coll.insert_one({
                    "email": email,
                    "password": password,
                    "consent": consent,
                    "consent_version": "v1.0"
                })
                messages.success(request, "Registro exitoso. Ahora inicia sesión.")
                return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "myapp/registro.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        usuario = users_coll.find_one({"email": email})
        if usuario and check_password(password, usuario["password"]):
            request.session["usuario_email"] = email
            return redirect("red_social")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, "myapp/login.html")

    return render(request, "myapp/login.html")


def bienvenido(request):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")  # 🔒 seguridad básica
    return render(request, "myapp/bienvenido.html", {"email": email})


def aviso(request):
    return render(request, "myapp/aviso.html")

def red_social(request):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    # Cargar publicaciones (ordenadas de más recientes a más antiguas)
    publicaciones = list(posts_coll.find().sort("_id", -1))

    return render(request, "myapp/red_social.html", {
        "usuario": email,
        "publicaciones": publicaciones
    })

def nueva_publicacion(request):
    if request.method == "POST":
        email = request.session.get("usuario_email")
        contenido = request.POST.get("contenido")

        if not email:
            return redirect("login")

        contenido = contenido.strip()
        if not contenido:
            messages.warning(request, "No puedes publicar algo vacío.")
            return redirect("red_social")

        # Insertar la nueva publicación
        posts_coll.insert_one({
            "autor": email,
            "contenido": contenido,
            "likes": 0
        })

        # Limpia mensajes previos para evitar acumulación
        storage = messages.get_messages(request)
        for _ in storage:
            pass

        messages.success(request, "Publicación creada con éxito.")
        return redirect("red_social")

    return redirect("red_social")

# Cerrar sesión
def cerrar_sesion(request):
    if "usuario_email" in request.session:
        request.session.flush()
        messages.info(request, "Sesión cerrada correctamente.")
    return redirect("login")
