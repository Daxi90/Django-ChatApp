from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Message
from django.contrib.auth.decorators import login_required
from .functions import create_message, login_user, logout_user, register_user

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        return create_message(request)
    
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    if request.method == 'POST':
        return login_user(request)
    else:
        redirect = request.GET.get('next')
        return render(request, 'auth/login.html', {'redirect': redirect})

def logout_view(request):
    return logout_user(request)

def register_view(request):
    if request.method == 'POST':
        return register_user(request)
    else:
        redirect = request.GET.get('next')
        return render(request, 'register/index.html', {'redirect': redirect})
