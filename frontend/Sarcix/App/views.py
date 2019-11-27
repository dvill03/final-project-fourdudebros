from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Run, Naive
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

    #heatmap
    if request.POST.get('heatmap') == 'heatmap':
        from scripts import django_heatmap_naive as hm
        #hm.getRunHeatmap('naive')
        html = hm.getRunHeatmap('naive')
        return render(request, 'run.html', {'heatmap': html})

    #map
    elif request.POST.get('map') == 'map':
        context['run1'] = Run.objects.all()

    #upload_run
    elif request.POST.get('data_file') == 'data_file':
        file=request.FILES.get('document', False)
        if (file):
            # Can't give a path becuase it's accepted as an in_memory_file. Store, run, then delete the run
            filepath = Path(settings.BASE_DIR + "/media/" + file.name)
            if not filepath.is_file():
                fs = FileSystemStorage()
                fs.save(file.name, file)
            from scripts import django_naive_push as push_run
            push_run.load("naive", filepath)
            os.remove(filepath)
        else:
            print ("BAD FILEPATH")

    print(context)
    return render(request, 'run.html', context)


@csrf_exempt
def run_modal(request):
    run_data = []
    run_name = request.POST.get('run_name', False)
    if request.method == "POST" and request.is_ajax():
        print("is ajax")
        run_data = list(Naive.objects.all().values()[:100]) #remove slice after fully completed

    else:
        print("not ajax")

    #print(context)
    return JsonResponse({"run": run_data, "run_name": run_name})

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
    if request.method == "POST" and request.is_ajax():
        file=request.FILES.get('data_file', False)
        run_name = request.POST.get('run_name', False)
        if (file):
            # Can't give a path becuase it's accepted as an in_memory_file. Store, run, then delete the run
            filepath = Path(settings.BASE_DIR + "/media/" + file.name)
            if not filepath.is_file():
                fs = FileSystemStorage()
                fs.save(file.name, file)
            sys.path.append(settings.BASE_DIR + "/../../python_scripts")
            import django_naive_push as push_run
            push_run.load(filepath, "naive")
            os.remove(filepath)
        else:
            print ("BAD REQUEST")

        response = JsonResponse(dict(request.POST.items()))
        print(response.content)
        return JsonResponse(dict(request.POST.items()))
    else:
        print("Not Ajax")

    return render(request, 'run.html')
