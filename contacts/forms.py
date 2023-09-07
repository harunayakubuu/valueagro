from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs = {'placeholder':'Name'}),
            'phone': forms.TextInput(attrs = {'placeholder':'Phone number'}),
            'email': forms.EmailInput(attrs = {'placeholder':'Email (Optional)'}),
            'subject': forms.Select(attrs = {'class':'form-select'}),
            'message': forms.Textarea(attrs = {'placeholder':'Message', 'rows':'5'}),
            }


class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['status',]