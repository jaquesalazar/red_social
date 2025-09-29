from django import forms
from .models import Usuario

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
