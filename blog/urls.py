from django.urls import path
from .views import (
    categories,
    category_create,
    category_edit,
    CategoryDeleteView,

    public_activities,
    public_activity_details,
    all_activities,
    activity_create,
    activity_edit,
    ActivityDeleteView
)


app_name = 'blog'


urlpatterns = [
    path('activities/', public_activities, name = 'public-activities'),
    path('all/activities/', all_activities, name = 'all-activities'),
    path('activity/create/form/', activity_create, name = 'activity-create'),
    path('activity/<str:slug>/', public_activity_details, name = 'public-activity-details'),
    path('activity/<int:id>/edit/', activity_edit, name = 'activity-edit'),
    path('activity/<int:id>/delete/', ActivityDeleteView.as_view(), name = 'activity-delete'),

    path('categories/', categories, name = 'categories'),
    path('category/create/form/', category_create, name = 'category-create'),
    path('category/<int:id>/edit/', category_edit, name = 'categoy-edit'),
    path('category/<int:id>/delete/', CategoryDeleteView.as_view(), name = 'category-delete')
]