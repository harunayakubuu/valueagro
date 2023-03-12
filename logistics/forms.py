from django import forms
from . models import Driver, Vehicle


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'email', 'phone', 'date_of_birth', 'driver_license', 'picture', 'status',)


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('category', 'vehicle_number', 'chasis_number', 'driver', 'picture', 'status',)