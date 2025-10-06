from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.contrib import messages

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.consent_version = "v1.0"  # registra la versión del aviso
            usuario.save()
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect("bienvenido")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = RegistroForm()
    return render(request, "myapp/registro.html", {"form": form})

@login_required(login_url="/registro/")
def bienvenido(request):
    # Solo usuarios logueados pueden acceder
    return render(request, "myapp/bienvenido.html")

def aviso(request):
    return render(request, "myapp/aviso.html")

