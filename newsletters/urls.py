from django.urls import path
from . import views 

app_name = 'newsletters'

urlpatterns = [
    path('email-list/', views.email_list, name = 'email_list'),
    path('subscription/form/', views.subscription_form, name = 'subscription_form'),
    path('message/form/', views.mail_message_form, name = 'mail_message_form'),
    path('messages/list/', views.mail_messages_list, name = 'mail_messages_list'),
]