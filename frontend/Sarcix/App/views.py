from django.shortcuts import render
from django.http import JsonResponse
from .models import Run
import psycopg2
from psycopg2.extras import RealDictCursor
import json

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

def get_runs(request):
    con = psycopg2.connect(database='sarcix_test_db', user='postgres', password='1601324', host='localhost', port='5432')
    cur = con.cursor(cursor_factory=RealDictCursor)
    #query_sql = "SELECT row_to_json(row) FROM (SELECT event_name, coverage_name, score FROM run1) as row LIMIT 5;" 
    query_sql = "SELECT event_name, coverage_name, score FROM run1 LIMIT 10"
    cur.execute(query_sql)
    results = cur.fetchall()
    
    #return json.dumps(cur.fetchall(), indent=2)
    return JsonResponse(results, safe=False)

def heatmap(request):
    return render(request, 'heatmap.html')