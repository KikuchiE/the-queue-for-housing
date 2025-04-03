from django.urls import path
from . import views

urlpatterns = [
    # Other paths...
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/', views.notification_details, name='notification_details'),
]