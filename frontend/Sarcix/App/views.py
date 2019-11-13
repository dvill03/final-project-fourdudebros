from django.shortcuts import render
from .models import Run
import psycopg2

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
    con = psycopg2.connect(database='sarcix_test_db', user='postgres', password='1601324', host='localhost', port='5432')
    cur = con.cursor()
    f = open('./static/js/data.csv', 'w')
    cur.copy_to(f, 'run1', columns=('event_name', 'coverage_name', 'score'), sep=",")
    con.commit()
    con.close()
    return render(request, 'heatmap.html')