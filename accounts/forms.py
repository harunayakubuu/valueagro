from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import Account, Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(min_length = 4, max_length = 50)
    email = forms.EmailField(min_length =12 , max_length = 50)
    class Meta:
        model = Account
        fields = ['email', 'username', 'phone_number', 'password1', 'password2']
        field_classes = {'username': UsernameField}

        widgets = {
            'email': forms.TextInput(attrs = {'class':'form-control'}),
            'username': forms.TextInput(attrs = {'class': 'form-control'}),
            'password1': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Password'}),
            'password2': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Password Confirmation'}),
        }

        help_texts = {
            'username': None,
        }


# Registering Staff User by the admin
class StaffUserCreateForm(forms.ModelForm):
    username = forms.CharField(min_length =12 , max_length = 50)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role')

        widgets = {
            'username': forms.TextInput(attrs = {'class': 'form-control'}),
            'email': forms.TextInput(attrs = {'class':'form-control'}),
            'role': forms.Select(attrs = {'class': 'form-select'}),
            'password1': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Password'}),
            'password2': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Password Confirmation'}),
        }

        help_texts = {
            'username': None,
        }


# All users account update (staff and customers)
class UserAccountEditForm(UserChangeForm):
    email = forms.EmailField(
        label = "Account email (cannot be changed)", min_length = 4, max_length = 50,
        widget = forms.TextInput(attrs = {'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email', 'readonly':'readonly'})
    )
    username = forms.CharField(
        label = "Username (cannot be changed)", min_length =4 , max_length = 50,
        widget = forms.TextInput(attrs = {'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly':'readonly'})
    )
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 'phone_number']


# All users profile update (staff and customers)
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['additional_phone_number', 'profile_picture']

        help_texts = {
            'username': None,
        }


# Updating User Role by the admin
class UserRoleEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', 'is_staff', 'is_superuser', 'role')

        widgets = {
            'role': forms.Select(attrs = {'class': 'form-select'}),
        }