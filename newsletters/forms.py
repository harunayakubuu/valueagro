from django import forms
from .models import Subscriber, MailMessage


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)

        widgets = {
            'title': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder':'Email'}),
        }

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        qs = Subscriber.objects.filter(email__iexact=email)
        if qs.exists():
            self.add_error('email', f"The email, '{email}' already exists.")
        return data


class SubscriptionEditForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)

        widgets = {
            'email': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Email'}),
        }


class MailMessageCreateForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ('title', 'message')

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Title'}),
            'message': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Message', 'rows':'5'}),
        }

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = MailMessage.objects.filter(title__iexact=title)
        if qs.exists():
            self.add_error('title', f"The title, '{title}' has already exist.")
        return data


class MailMessageEditForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ('title', 'message', 'active')

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Title'}),
            'message': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Message', 'rows':'5'}),
            }