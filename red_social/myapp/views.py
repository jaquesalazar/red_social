from django.shortcuts import render, redirect
from .forms import RegistroForm
from mongo import users_coll
from django.contrib.auth.hashers import make_password

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = make_password(form.cleaned_data["password"])
            consent = form.cleaned_data["consent"]

            # Verificar si el usuario ya existe
            if users_coll.find_one({"email": email}):
                form.add_error("email", "Este correo ya está registrado.")
            else:
                usuario_doc = {
                    "email": email,
                    "password": password,
                    "consent": consent,
                    "consent_version": "v1.0"
                }
                users_coll.insert_one(usuario_doc)
                return redirect("bienvenido")
    else:
        form = RegistroForm()
    return render(request, "myapp/registro.html", {"form": form})

def bienvenido(request):
    return render(request, "myapp/bienvenido.html")

def aviso(request):
    return render(request, "myapp/aviso.html")
