from django.urls import path
from . import views

app_name = 'housing_units'

urlpatterns = [
    path('', views.housing_units_list, name='housing-units-list'),
    path('create/', views.create_housing_unit, name='create-unit'),
    path('<int:unit_id>/', views.view_housing_unit, name='view-unit'),
    path('<int:unit_id>/edit/', views.edit_housing_unit, name='edit-unit'),
]
