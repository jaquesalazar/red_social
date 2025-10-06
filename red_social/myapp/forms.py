from django import forms
from .models import Usuario
import re
from django.contrib.auth.hashers import make_password

class RegistroForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label="He leído y acepto el Aviso de Privacidad"
    )

    class Meta:
        model = Usuario
        fields = ["email", "password", "consent"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # Reglas de seguridad
        if len(password) < 10:
            raise forms.ValidationError("La contraseña debe tener al menos 10 caracteres.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Debe contener al menos un número.")
        if not re.search(r"[!@#$%&*]", password):
            raise forms.ValidationError("Debe contener al menos un carácter especial.")
        return password
