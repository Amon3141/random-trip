from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from randomtrip.models import CustomUser, Trip, Activity
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .python_functions.get_random_site import get_random_site


def roulette_view(request):
  return render(request, 'roulette.html')

def next_destination_view(request):
  return render(request, 'next_destination.html')

def moving_view(request):
  return render(request, 'moving.html')

def custom_login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valie():
      user = form.get_user()
      login(request, user)
      return redirect('home')
  else:
    form = AuthenticationForm()
  
  return render(request, 'login.html', {'form': form})

@csrf_exempt
@require_POST
def provide_random_site(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      current_latitude = data.get('latitude')
      current_longitude = data.get('longitude')
      radius = data.get('radius')
      
      name, address, description, homepage = get_random_site(current_latitude, current_longitude, radius)
      
      if name is not None:
        response_data = {
          'name': name,
          'address': address,
          'description': description,
          'homepage': homepage,
          'google_maps_url': f"https://www.google.com/maps/dir/?api=1&origin=Current+Location&destination={name}"
        }
        return JsonResponse(response_data)
      else:
        return JsonResponse({'error': 'No site was found'}, status=404)
      
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid data was sent'}, status=400)
  
  return JsonResponse({'error': 'POST request is required'}, status=405)