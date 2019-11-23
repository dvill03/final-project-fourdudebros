from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from .models import Run
from pathlib import Path
from filebrowser.base import FileObject
import psycopg2, json, sys, os


# home
def home(request):
    if request.POST.get('reports') == 'Reports':

        #tables = connection.introspection.table_names()
        #seen_models = connection.introspection.installed_models(tables)
        return HttpResponse(status=204)

    if request.POST.get('Next') == 'Next':
        print("\nFirst event_name:", run[0].event_name, "\nFirst coverage_name:", run[0].coverage_name, "\nFirst score:", run[0].score, "\n")
        return HttpResponse(status=204)

    return render(request, 'home.html')

# run
def run(request):
    context = {}

    #map
    if request.POST.get('map') == 'map':
        context['run1'] = Run.objects.all()
        print('map')

    #upload_run
    elif request.POST.get('data_file') == 'data_file':
        file=request.FILES.get('document', False)
        if (file):
            # Can't give a path becuase it's accepted as an in_memory_file. Store, run, then delete the run
            filepath = Path(settings.BASE_DIR + "/media/" + file.name)
            if not filepath.is_file():
                fs = FileSystemStorage()
                fs.save(file.name, file)
            sys.path.append(settings.BASE_DIR + "/../../python_scripts")
            import django_test_push_a_run as push_run
            push_run.load(filepath)
            os.remove(filepath)
        else:
            print ("BAD FILEPATH")

    print(context)
    return render(request, 'run.html', context)

def run_modal(request):
    context = {}
    context['run1'] = Run.objects.all()
    context['modal'] = True
    return render(request, 'run.html', context)

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

#
def get_runs(request):
    con = psycopg2.connect(database='sarcix_test_db', user='postgres', password='2345', host='localhost', port='5432')
    cur = con.cursor()
    query_sql = "SELECT row_to_json(row) FROM (SELECT event_name, coverage_name, score FROM run1) row LIMIT 2;"
    cur.execute(query_sql)
    results = cur.fetchall()
    print(results)
    return JsonResponse(results, safe=False)

def heatmap(request):
    return render(request, 'heatmap.html')

@csrf_protect
def push_run_script(request):
    #file = dict(request.POST.items())['file']
    #file.path
    #print(file)
    print(request.FILES)
    if request.method == "POST" and request.is_ajax():
        print("Ajax")
        file=request.FILES.get('my_file', False)
        if (file):
            print("File")
        else:
            print("No file")
        response = JsonResponse(dict(request.POST.items()))
        print(response.content)
        return JsonResponse(dict(request.POST.items()))
    else:
        print("Not Ajax")

    return render(request, 'run.html')
