from django.urls import path
from . import views

app_name = 'randomtrip'

urlpatterns = [
  #path('login/', views.custom_login_view, name='login'),
  path('roulette/', views.roulette_view, name='roulette'),
  path('next-destination/', views.next_destination_view, name='next-destination'),
  path('moving/', views.moving_view, name='moving'),
  path('api/get-random-site', views.provide_random_site, name='get-random-site'),
]