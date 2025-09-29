from django.shortcuts import render, redirect
from .forms import RegistroForm

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.consent_version = "v1.0"
            usuario.save()
            return redirect("bienvenido")
    else:
        form = RegistroForm()
    return render(request, "myapp/registro.html", {"form": form})

def bienvenido(request):
    return render(request, "myapp/bienvenido.html")

def aviso(request):
    return render(request, "myapp/aviso.html")

