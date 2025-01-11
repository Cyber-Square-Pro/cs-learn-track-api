from django.db import models

class AdminData(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
