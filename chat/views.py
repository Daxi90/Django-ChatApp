from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("Received data: " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    
    
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            if redirect is not None:
                return HttpResponseRedirect(request.POST.get('redirect'))
            else:
                return HttpResponseRedirect('/chat')
        else:
            return render(request, 'auth/login.html',{'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def register_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.full_clean()  # Validiert das Modell (wirft ValidationError bei Fehlschlag)
            user.save()

            serialized_obj = serializers.serialize('json', [user])
            return JsonResponse(serialized_obj[1:-1], safe=False)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "error": "The user name already exists."}, status=400)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "error": "Invalid data: " + str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "error": "Unbekannter Fehler: " + str(e)}, status=500)
    else:
        return render(request, 'register/index.html', {'redirect': redirect})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
    # Redirect to a success page.