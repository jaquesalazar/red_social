from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegistroForm
from mongo import users_coll, posts_coll
from bson import ObjectId
from django.views.decorators.http import require_POST


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


def red_social(request):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    publicaciones = list(posts_coll.find().sort("_id", -1))
    for p in publicaciones:
        p["id"] = str(p["_id"])
        # Inicializar likes y comentarios si no existen
        if "likes" not in p or not isinstance(p["likes"], list):
            p["likes"] = []
        if "comentarios" not in p or not isinstance(p["comentarios"], list):
            p["comentarios"] = []

    return render(request, "myapp/red_social.html", {
        "usuario": email,
        "publicaciones": publicaciones
    })


def nueva_publicacion(request):
    if request.method == "POST":
        email = request.session.get("usuario_email")
        if not email:
            return redirect("login")

        contenido = request.POST.get("contenido", "").strip()
        if not contenido:
            messages.warning(request, "No puedes publicar algo vacío.")
            return redirect("red_social")

        posts_coll.insert_one({
            "autor": email,
            "contenido": contenido,
            "likes": [],
            "comentarios": []
        })

        messages.success(request, "Publicación creada con éxito.")
        return redirect("red_social")

    return redirect("red_social")


def cerrar_sesion(request):
    if "usuario_email" in request.session:
        request.session.flush()
        messages.info(request, "Sesión cerrada correctamente.")
    return redirect("login")


@require_POST
def dar_like(request, post_id):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    post = posts_coll.find_one({"_id": ObjectId(post_id)})
    if post and post["autor"] != email:
        likes = post.get("likes", [])
        if email in likes:
            # Quitar like
            likes.remove(email)
        else:
            # Agregar like
            likes.append(email)
        posts_coll.update_one({"_id": ObjectId(post_id)}, {"$set": {"likes": likes}})
    return redirect("red_social")



@require_POST
def comentar_publicacion(request, post_id):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    contenido = request.POST.get("comentario", "").strip()
    if not contenido:
        messages.warning(request, "El comentario no puede estar vacío.")
        return redirect("red_social")

    post = posts_coll.find_one({"_id": ObjectId(post_id)})
    if post and post["autor"] != email:
        comentario = {"autor": email, "contenido": contenido}
        comentarios = post.get("comentarios", [])
        comentarios.append(comentario)
        posts_coll.update_one({"_id": ObjectId(post_id)}, {"$set": {"comentarios": comentarios}})
    return redirect("red_social")


@require_POST
def eliminar_publicacion(request, post_id):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")

    post = posts_coll.find_one({"_id": ObjectId(post_id)})
    if post and post["autor"] == email:
        posts_coll.delete_one({"_id": ObjectId(post_id)})
        messages.success(request, "Publicación eliminada.")
    return redirect("red_social")


def bienvenido(request):
    email = request.session.get("usuario_email")
    if not email:
        return redirect("login")  # 🔒 seguridad básica
    return render(request, "myapp/bienvenido.html", {"email": email})

def aviso(request):
    return render(request, "myapp/aviso.html")