from django.urls import path
from . views import (
    account_activate,
    dashboard,
    profile,
    CustomerKYCWizardView,
    users,
    staff_user_create,
    user_details,
    user_role_edit,
    user_account_edit,
    account_delete,
    account_delete_confirm,
    UserDeleteView,
    account_success,
    agro_dealers,
    agro_dealer_details
)

app_name = "accounts"


urlpatterns = [
    path('dashboard/', dashboard, name = 'dashboard'),
    path('profile/', profile, name = 'profile'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name = 'account-activate'),
    path('customer-kyc/form/', CustomerKYCWizardView.as_view(), name = 'customer-kyc-form'),
    path('customers/agro-dealers/<int:id>/', agro_dealer_details, name = 'agro-dealer-details'),
    path('customers/agro-dealers/', agro_dealers, name = 'agro-dealers'),
    
    path('users/', users, name = 'users'),
    path('users/staff/user/create/form/', staff_user_create, name = 'staff-user-create'),
    path('users/user/<str:username>/', user_details, name = 'user-details'),
    path('users/user/<int:id>/role/edit/', user_role_edit, name = 'user-role-edit'),
    path('user/edit/', user_account_edit, name = 'user-account-edit'),
    path('account/delete/', account_delete, name = 'account-delete'),
    path('account/delete/confirm/', account_delete_confirm, name = 'account-delete-confirm'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name = 'user-delete'),
    path('account-success/', account_success, name = 'account-success'),
]