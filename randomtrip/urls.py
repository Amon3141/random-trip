from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
  path('', views.randomtrip, name='randomtrip'),
  path('option_screen/', views.option_screen, name='option_screen'),
]