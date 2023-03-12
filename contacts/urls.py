from django.urls import path
from . import views 

app_name = 'contacts'

urlpatterns = [
    path('contact/form/', views.contact_form, name = 'contact-form'),
    path('contact/messages/', views.contact_messages, name = 'contact-messages'),
    path('contact/message/<int:id>/details/', views.contact_message_detail, name = 'contact-message-details'),
    path('contact/message/<int:id>/update/', views.contact_message_update, name = 'contact-message-update'),
    path('contact/message/<int:pk>/delete/', views.ContactMessageDeleteView.as_view(), name = 'contact-message-delete'),
]