from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=21, decimal_places=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=100)

    class Meta:
        unique_together = [["user", "currency"]]


class Instrument(models.Model):
    name = models.CharField(max_length=10)


class Symbol(models.Model):
    ticker = models.CharField(max_length=10)
    description = models.TextField(null=True)
    base_instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT, related_name="+")
    quoting_instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT, related_name="+")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=21, decimal_places=8)
    price = models.DecimalField(max_digits=21, decimal_places=8)

    class OrderSide(models.TextChoices):
        Buy = 'BUY'
        Sell = 'SELL'

    side = models.CharField(max_length=4, choices=OrderSide.choices)
