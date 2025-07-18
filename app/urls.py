from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="index"),
  path('cities/', views.get_cities, name='cities'),
  path('cities/<int:id>/', views.get_city, name='cities'),
  path('states/', views.get_states, name='states'),
]