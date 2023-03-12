from django.urls import path
from . views import partner_list, partner_details, partner_create, partner_edit, partner_delete

app_name = 'partners'

urlpatterns = [
    path('', partner_list, name = 'partner-list'),
]