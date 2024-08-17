from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  def __str__(self):
    return self.username

# Create your models here.
class Trip(models.Model):
  title = models.CharField(max_length=50)
  traveler = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.title
  
class Activity(models.Model):
  TOURISM = 'Tourism'
  FOOD = 'Food'
  LODGING = 'Lodging'
  TYPE_CHOICES = [
    (TOURISM, 'TOURISM'),
    (FOOD, 'FOOD'),
    (LODGING, 'LODGING'),
  ]
  
  title = models.CharField(max_length=100)
  type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=TOURISM)
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
  
  def __str__(self):
    return self.title
  