from django.contrib.auth.models import AbstractUser
from django.db import models


class customuser(AbstractUser):
    codice_fiscale = models.CharField(max_length=16, blank=True, null=True)
    nome = models.CharField(max_length=40)
    cognome = models.CharField(max_length=40)