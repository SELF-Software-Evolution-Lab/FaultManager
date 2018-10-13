from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
import json
from django.db import connection
from .utils.graphdata import Graphdata
from django.http import JsonResponse

# Get data structure with information to build Fault Types Graph
def getDataFaultTypes():
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_event.type_id"
            + " GROUP BY type_id;")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({"name": row[0], "y": row[1]})

    return data    

# Get data structure with information to build Url per Fault Types Graph
def getDataUrlFaults():
    with connection.cursor() as cursor:
        cursor.execute("SELECT url, DATE(time), count(0)"
            + " FROM iotfaults_event"
            + " GROUP BY url, DATE(time);")
        rows = cursor.fetchall()
        
        graphData = Graphdata(0)
        graphData.load(rows)
        
        data = {}
        data["categories"] = graphData.get_categories()
        data["series"] = graphData.get_series()
    return data    

# View for dinamic graphics
def index(request):
    #events = Event.objects.all()[:10]
    context = {
        'title': 'Dashboard',
        #'events': events,
        #'dataGraphPieFaultTypes': json.dumps(getDataFaultTypes()) ,
        #'dataGraphLineUrlFaults': json.dumps(getDataUrlFaults()) ,
    }
    return render(request, 'iotfaults/index.html', context)

# View for static graphics
def staticGraphs(request):
    #events = Event.objects.all()[:10]
    context = {
        'title': 'Dashboard',
        #'events': events,
        #'dataGraphPieFaultTypes': json.dumps(getDataFaultTypes()) ,
        #'dataGraphLineUrlFaults': json.dumps(getDataUrlFaults()) ,
    }
    return render(request, 'iotfaults/static_graphs.html', context)

def details(request, id):
    event = Event.objects.get(id=id) 
    context = {
        'event': event,
    }
    return render(request, 'iotfaults/details.html', context)
    
def jsonDataFaultTypes(request):
    data = getDataFaultTypes()
    return JsonResponse(data, safe=False)
    
def jsonDataUrlFaults(request):
    data = getDataUrlFaults()
    return JsonResponse(data, safe=False)    