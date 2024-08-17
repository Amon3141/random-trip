from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from randomtrip.models import CustomUser, Trip, Activity
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.
def randomtrip(request):
  return render(request, 'randomtrip.html')

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



def option_screen(request):
  return render(request, 'option_screen.html')

def test_screen(request):
  return render(request, 'test.html')

@csrf_exempt
@require_POST
def add_new_activity(request):
  try:
    data = json.loads(request.body)
    Activity.objects.create(
      title = data['title'],
      type = data['type'],
    )
    response = {'message': 'Added a new activity successfully'}
    return JsonResponse(response, status=201)
  except KeyError as e:
    return JsonResponse({'error': f'Missing field: {e.args[0]}'}, status=400)
  except Exception as e:
    return JsonResponse({'error': str(e)}, status=500)