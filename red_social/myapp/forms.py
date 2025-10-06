from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
import re

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmar Contraseña"
    )
    consent = forms.BooleanField(
        required=True,
        label="He leído y acepto el Aviso de Privacidad"
    )

    class Meta:
        model = Usuario
        fields = ["email", "nombre", "telefono", "direccion", "consent"]

    def clean_password2(self):
        pwd1 = self.cleaned_data.get("password1")
        pwd2 = self.cleaned_data.get("password2")
        if pwd1 != pwd2:
            raise ValidationError("Las contraseñas no coinciden")
        # Validación de contraseña fuerte: 8+ caracteres, 1 mayúscula, 1 número
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', pwd1):
            raise ValidationError("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número")
        return pwd2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data["password1"]  # se hasheará en models.py
        if commit:
            user.save()
        return user
