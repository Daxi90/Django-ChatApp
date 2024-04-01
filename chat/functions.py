from django.shortcuts import get_object_or_404
from .models import Message, Chat
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core import serializers

def create_message(request):
    print("Received data: " + request.POST['textmessage'])
    myChat = get_object_or_404(Chat, id=1)
    receiver = get_object_or_404(User, username='helpuser')
    
    new_message = Message.objects.create(
        text=request.POST['textmessage'],
        chat=myChat,
        author=request.user,
        receiver=receiver
    )
    serialized_obj = serializers.serialize('json', [new_message])
    return JsonResponse(serialized_obj[1:-1], safe=False)


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({"success": True, "message": "Login erfolgreich."})
    else:
        return JsonResponse({"error": "Login fehlgeschlagen. Benutzername oder Passwort ist falsch."}, status=401)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')

def register_user(request):
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
    except IntegrityError:
        return JsonResponse({"status": "failed", "error": "The user name already exists."}, status=400)
    except ValidationError as e:
        return JsonResponse({"status": "failed", "error": "Invalid data: " + str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"status": "failed", "error": "Unbekannter Fehler: " + str(e)}, status=500)