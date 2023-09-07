from django.urls import path
from . import views

app_name = "pages"


urlpatterns = [
    path('', views.index, name = 'index'),
    path('about-us/', views.about_us, name = 'about-us'),

    path('privacy-policy/', views.privacy_policy, name = 'privacy-policy'),
    path('policies/', views.policies, name = 'policies'),
    path('policy/create/', views.policy_create, name = 'policy-create'),
    path('policy/<int:id>/edit/', views.policy_edit, name = 'policy-edit'),

    path('terms-and-conditions/', views.t_and_c, name = 'terms-and-conditions'),
    path('terms/', views.terms, name = 'terms'),
    path('terms/create/', views.terms_create, name = 'terms-create'),
    path('terms/<int:id>/edit/', views.terms_edit, name = 'terms-edit'),
    
    path('service/add/', views.service_create, name = 'service-add'),
    path('service/<int:id>/edit/', views.service_edit, name = 'service-edit'),
    path('service/<int:id>/details/', views.service_details, name = 'service-details'),
    path('services-list/', views.services_list, name = 'services-list'),
    path('services/', views.services, name = 'services'),
    
    path('our-team/', views.team, name = 'team'),
    path('team/member/<str:member_id>/', views.team_member_details, name = 'team-member-details'),
    path('client/feedback/form/', views.testimonial_form, name = 'testimonial-form'),
]