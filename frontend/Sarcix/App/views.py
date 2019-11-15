from django.shortcuts import render
from .models import Run

# Create your views here.

def home(request):
    run = Run.objects.all()
    print(Run.objects.first().event_name) 
    return render(request, 'home.html', {'run': run})

def run(request):
    run = Run.objects.all()
    return render(request, 'run.html')

def reports(request):
    run = Run.objects.all()
    return render(request, 'reports.html')

def analysis(request):
    run = Run.objects.all()
    return render(request, 'analysis.html')

def compare(request):
    run = Run.objects.all()
    return render(request, 'compare.html')

def prepare(request):
    run = Run.objects.all()
    return render(request, 'prepare.html')

def setup(request):
    run = Run.objects.all()
    return render(request, 'setup.html')

def help(request):
    run = Run.objects.all()
    return render(request, 'help.html')
