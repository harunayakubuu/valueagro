from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import Account, CompanyInformation, WarehouseInformation, ShopInformation, Profile


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


class CompanyInformationForm(forms.ModelForm):

    BOOL_CHOICES = [('True', 'Yes'), ('False', 'No')]
    warehouse_available = forms.BooleanField(
        widget=forms.RadioSelect(choices=BOOL_CHOICES),
        required=False
    )

    class Meta:
        model = CompanyInformation
        # fields = "__all__"
        fields = [
            'company_name', 'state', 'lga', 'town_city', 'address',
            'phone', 'email', 'website', 'company_type', 
            'nature_of_business', 'company_registration_number', 
            'tax_registration_number', 'fss_registration_number', 
        ]

        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
            'company_type': forms.Select(attrs = {'class': 'form-select'}),
        }


class WarehouseInformationForm(forms.ModelForm):
    class Meta:
        model = WarehouseInformation
        # fields = "__all__"
        fields = [
            'address', 'state', 'lga', 'town_city', 
            'warehouse_manager', 'manager_phone', 
            'manager_email', 'picture' 
        ]

        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
        }


class ShopInformationForm(forms.ModelForm):
    class Meta:
        model = ShopInformation
        fields = [
            'address', 'state', 'lga', 'town_city', 
            'shop_keeper', 'shop_keeper_phone', 
            'shop_keeper_email', 'picture',
        ]

        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
        }