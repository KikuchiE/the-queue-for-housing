from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('check-queue/', views.check_queue, name='check-queue'),
    path('list-queue/', views.list_queue, name='list-queue'),
    path('my-application/list/', views.my_applications, name='my-applications-list'),
    path('my-application/create', views.create_application, name="create-application"),
    path('my-application/<int:application_id>/', views.view_application, name='view-application'),
]