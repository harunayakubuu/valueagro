from django import forms
from .models import DeliveryAddress


class AddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['state', 'city', 'address', 'is_primary']