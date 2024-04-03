from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required
from .functions import create_message, login_user, logout_user, register_user

@login_required(login_url='/login/')
def index(request):
    """
    View for the chat index page. This view handles displaying chat messages for a specific chat.

    If the request method is POST, it calls the create_message function to handle the message creation process.
    Otherwise, it retrieves messages from the database filtering by chat ID (hardcoded as 1 for this example),
    and renders them using the 'chat/index.html' template.

    Requires user to be logged in, redirecting to the login page if not authenticated.

    Parameters:
    - request: HttpRequest object.

    Returns:
    - HttpResponse object with rendered chat page or a redirect to message creation.
    """
    if request.method == 'POST':
        return create_message(request)
    
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    """
    View for handling user login. It supports both GET and POST requests.

    On POST, attempts to log in the user using the login_user function.
    On GET, renders the login page. It can also handle a 'next' GET parameter for redirecting the user
    after a successful login.

    Parameters:
    - request: HttpRequest object.

    Returns:
    - HttpResponse object either redirecting to the 'next' page or rendering the login page.
    """
    if request.method == 'POST':
        return login_user(request)
    else:
        redirect = request.GET.get('next')
        return render(request, 'auth/login.html', {'redirect': redirect})

def logout_view(request):
    """
    View for handling user logout.

    Calls the logout_user function to log out the user.

    Parameters:
    - request: HttpRequest object.

    Returns:
    - HttpResponse object returned by logout_user function.
    """
    return logout_user(request)

def register_view(request):
    """
    View for handling user registration. Supports both GET and POST requests.

    On POST, attempts to register the user using the register_user function.
    On GET, renders the registration page. Similar to the login view, it can handle a 'next' GET parameter
    for redirecting after successful registration.

    Parameters:
    - request: HttpRequest object.

    Returns:
    - HttpResponse object either redirecting to the 'next' page or rendering the registration page.
    """
    if request.method == 'POST':
        return register_user(request)
    else:
        redirect = request.GET.get('next')
        return render(request, 'register/index.html', {'redirect': redirect})
