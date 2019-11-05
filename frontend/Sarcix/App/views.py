from django.shortcuts import render
from .models import Run

# Create your views here.

def home(request):
    runs = Run.objects.all()
    return render(request, 'home.html', {'runs': runs})
