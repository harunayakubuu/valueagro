from django.urls import path
from . views import addresses, address_add, address_edit, address_delete


app_name = "addresses"


urlpatterns = [
    path('', addresses, name = 'address-list'),
    path('add/', address_add, name = 'address-add'),
    path('<int:id>/edit/', address_edit, name = 'address-edit'),
    path('<int:id>/delete/', address_delete, name = 'address-delete'),
]