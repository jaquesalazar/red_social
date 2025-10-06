from django.db import models

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # hashear la contraseña
    consent = models.BooleanField(default=False)
    consent_version = models.CharField(max_length=10, default="v1.0")
    consent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
