from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
#singup view
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from request
            username = data['username']
            email = data['email']
            password = data['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Create user (password is hashed automatically)
        user = User.objects.create_user(username=username, email=email, password=password)

        # Optional: auto-login after signup
        login(request, user)

        return JsonResponse({'message': 'User created successfully and logged in'}, status=201)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)



#login view
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # Create session
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
