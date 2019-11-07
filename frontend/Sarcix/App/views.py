from django.shortcuts import render
from .models import Run

# Create your views here.

def home(request):
    runs = Run.objects.all()
    return render(request, 'home.html', {'runs': runs})

def run(request):
    return render(request, 'run.html')

def reports(request):
    return render(request, 'reports.html')

def analysis(request):
    return render(request, 'analysis.html')

def compare(request):
    return render(request, 'compare.html')

def prepare(request):
    return render(request, 'prepare.html')

def setup(request):
    return render(request, 'setup.html')

def help(request):
    return render(request, 'help.html')

def heatmap(request):
    #data
    return render(request, 'heatmap.html')