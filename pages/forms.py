from django import forms
from .models import PrivacyPolicy, Service, TermsAndCondition, AboutUs, Testimonial


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = ['about']

        widgets = {
            'policy': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Policy', 'rows':'4'}),
            }

class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['policy', 'active']

        widgets = {
            'policy': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Policy', 'rows':'4'}),
            }
    

class PrivacyPolicyEditForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['policy', 'active']

        widgets = {
            'policy': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Policy', 'rows':'4'}),
            }


class TermsAndConditionForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = ['terms_and_conditions', 'active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }
    

class TermsAndConditionEditForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = ['terms_and_conditions', 'active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }
    

class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['testimony']

        widgets = {
            'testimony': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Feedback', 'rows':'4'}),
            }