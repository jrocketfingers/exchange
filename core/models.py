from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=21, decimal_places=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
