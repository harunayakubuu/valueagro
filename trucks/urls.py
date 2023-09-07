from django.urls import path
from .views import truck_summary, truck_add, truck_delete, truck_update


app_name = 'trucks'


urlpatterns = [
    path('add/', truck_add, name = 'truck-add'),
    path('delete/', truck_delete, name = 'truck-delete'),
    path('update/', truck_update, name = 'truck-update'),
    path('summary/', truck_summary, name = 'truck-summary'),
]