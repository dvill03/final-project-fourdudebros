from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Run, Naive
from pathlib import Path
from filebrowser.base import FileObject
from psycopg2.extras import RealDictCursor
import psycopg2, json, sys, os

# home
def home(request):
    return render(request, 'home.html')

# run
def run(request):
    return render(request, 'run.html')


@csrf_exempt
def run_modal(request):
    run_data = []
    run_name = request.GET.get('run', False)
    if request.method == "GET" and request.is_ajax():
        if (request.GET.get('modal_type') == 'naive'):
            run_data = list(Naive.objects.filter(pk=run_name).values())
        else:
            run_data = list(Run.objects.all().values())
    else:
        print("not ajax")

    #print(context)
    return JsonResponse({"run": run_data})

# reports
def reports(request):
    return render(request, 'reports.html')

# analysis
def analysis(request):
    return render(request, 'analysis.html')

# compare
def compare(request):
    return render(request, 'compare.html')

# prepare
def prepare(request):
    return render(request, 'prepare.html')

# setup
def setup(request):
    return render(request, 'setup.html')

# help
def help(request):
    return render(request, 'help.html')

def get_runs(request):
    con = psycopg2.connect(database='sarcix_test_db', user='postgres', password='2345', host='localhost', port='5432')
    cur = con.cursor(cursor_factory=RealDictCursor)
    query_sql = "SELECT event_name, coverage_name, score FROM run1" #44650 total
    cur.execute(query_sql)
    results = cur.fetchall()
    return JsonResponse(results, safe=False)

# Dropdowns
def dropdowns(request):
    runs = list(Naive.objects.values("run_name").distinct())
    return JsonResponse(runs, safe=False)


# Heatmap
def get_analysis(request):
    from scripts import django_heatmap_naive as hm
    heatmap = hm.getRunHeatmap(request.GET.get('run'))
    return JsonResponse(heatmap, safe=False)

def heatmap(request):
    return render(request, 'heatmap.html')

@csrf_protect
def push_run_script(request):
    if request.method == "POST" and request.is_ajax():
        file=request.FILES.get('data_file', False)
        run_name = request.POST.get('run_name', False)
        if (file):
            # Can't give a path becuase it's accepted as an in_memory_file. Store, run, then delete the run
            filepath = Path(settings.BASE_DIR + "/media/" + file.name)
            if not filepath.is_file():
                fs = FileSystemStorage()
                fs.save(file.name, file)
            from scripts import django_naive_push as push_run
            push_run.load(filepath, run_name)
            os.remove(filepath)
        else:
            print ("BAD REQUEST")
        return JsonResponse(dict(request.POST.items()))
    else:
        print("Not Ajax")

    return render(request, 'run.html')
