from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
  path('', views.randomtrip, name='randomtrip'),
  path('option_screen/', views.option_screen, name='option_screen'),
  path('test/', views.test_screen, name='test'),
  path('add-new-activity/', views.add_new_activity, name='add_new_activity'),
  path('login/', views.custom_login_view, name='login')
]