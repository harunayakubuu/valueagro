from django import forms
from .models import Partner


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'about', 'website', 'active']

        widgets = {
            'name': forms.TextInput(attrs = {'placeholder':'Name'}),
            'about': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'About partner', 'rows':'4'}),
            
            }