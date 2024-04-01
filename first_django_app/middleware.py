from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError

class DatenbankCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Versuche, eine Verbindung zur Standarddatenbank herzustellen
            connections['default'].cursor()
        except OperationalError:
            # Wenn ein OperationalError auftritt, ist die Datenbank nicht verfügbar
            return HttpResponse("Entschuldigung, die Datenbank ist gerade nicht verfügbar.", status=503)

        response = self.get_response(request)
        return response
