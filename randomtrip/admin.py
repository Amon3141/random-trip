from django.contrib import admin
from .models import CustomUser, Trip, Activity

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Trip)
admin.site.register(Activity)