from django.db import models
from accounts.models import Profile
from products.choices import STATE_CHOICES
from django.conf import settings


class DeliveryAddress(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    state = models.CharField(max_length = 20, choices = STATE_CHOICES)
    city = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    is_primary = models.BooleanField(default = False, verbose_name="Primay Address?")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user}'