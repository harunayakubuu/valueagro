from django.urls import path
from . views import partners, partner_list, partner_details, partner_create, partner_edit, partner_delete

app_name = 'partners'

urlpatterns = [
    path('', partners, name = 'partners'),
    path('list/', partner_list, name = 'partner-list'),
    path('create/form/', partner_create, name = 'partner-create'),
    path('partner/<str:slug>/', partner_details, name = 'partner-details'),
]