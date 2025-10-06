from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    # Información personal
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    
    # Contraseña
    password = models.CharField(max_length=128)  # se guardará hasheada

    # Consentimiento de privacidad
    consent = models.BooleanField(default=False)
    consent_version = models.CharField(max_length=10, default="v1.0")
    consent_date = models.DateTimeField(auto_now_add=True)

    # Control de acceso
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Hashea la contraseña si aún no está hasheada
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
