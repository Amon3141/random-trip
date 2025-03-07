from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from randomtrip.models import CustomUser, Trip, Activity
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .python_functions.get_random_site import get_random_site
import math
from django.contrib.auth.decorators import login_required

@login_required
def roulette_view(request):
  return render(request, 'roulette.html')

@login_required
def next_destination_view(request):
  show_homepage = request.GET.get('show_homepage', 'false')
  context = {
    'show_homepage': show_homepage,
  }
  return render(request, 'next_destination.html', context)

@login_required
def moving_view(request):
  destination = request.GET.get('destination', '東京タワー')
  context = {
    'destination': destination,
  }
  return render(request, 'moving.html', context)

@csrf_exempt
@require_POST
def provide_random_site(request):
  print("called")
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      current_latitude = data.get('latitude')
      current_longitude = data.get('longitude')
      radius = data.get('radius')
      
      name, address, description, homepage = get_random_site(current_latitude, current_longitude, radius)
      
      def is_not_nan(value):
        return value == value and not isinstance(value, float) or not math.isnan(value)
      
      if name is not None:
        response_data = {
          'name': name if is_not_nan(name) else '',
          'address': address if is_not_nan(address) else '',
          'description': description if is_not_nan(description) else '',
          'homepage': homepage if is_not_nan(homepage) else '',
          'google_maps_url': f"https://www.google.com/maps/dir/?api=1&origin=Current+Location&destination={name}" if is_not_nan(name) else ''
        }
        return JsonResponse(response_data)
      else:
        return JsonResponse({'error': 'No site was found'}, status=404)
      
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid data was sent'}, status=400)
  
  return JsonResponse({'error': 'POST request is required'}, status=405)