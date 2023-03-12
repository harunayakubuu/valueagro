from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Name'}),
            'phone': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Phone number'}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder':'Email (Optional)'}),
            # 'subject': forms.Select(attrs = {'class': 'form-select'}),
            'message': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Message', 'rows':'5'}),
            }


class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['status',]