from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.
def randomtrip(request):
  return render(request, 'randomtrip.html')

def option_screen(request):
    return render(request, 'option_screen.html')