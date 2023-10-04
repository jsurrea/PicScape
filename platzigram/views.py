"""Platzigram views."""

# Django
from django.http import HttpResponse

# Utilities
from datetime import datetime

def hello_world(request):
    """Return a greeting."""
    return HttpResponse('Oh, hi! Current server time is {now}'.format(
        now=datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
    ))

def hi(request):
    """Hi."""
    return HttpResponse(request.GET["numbers"])
