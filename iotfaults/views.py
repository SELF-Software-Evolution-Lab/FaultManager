from django.shortcuts import render
from django.http import HttpResponse
from .models import Alarm
import json
from django.db import connection
from .utils.graphdata import Graphdata

# Get data structure with information to build Fault Types Graph
def getDataFaultTypes():
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.name, count(0)"
            + " FROM iotfaults_alarm"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_alarm.type_id"
            + " GROUP BY type_id;")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({"name": row[0], "y": row[1]})

    return data    

# Get data structure with information to build Fault Device Types with Faults Graph
def getDataFaultDeviceTypes():
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_devicetype.name, count(0)"
            + " FROM iotfaults_alarm"
            + " INNER JOIN iotfaults_devicetype"
            + " ON iotfaults_devicetype.id = iotfaults_alarm.deviceType_id"
            + " GROUP BY deviceType_id;")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({"name": row[0], "y": row[1]})

    return data    

# Get data structure with information to build Device per Fault Types Graph
def getDataDeviceFaultTypes():
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.name, iotfaults_devicetype.name, count(0)"
            + " FROM iotfaults_alarm"
            + " INNER JOIN iotfaults_devicetype"
            + " ON iotfaults_devicetype.id = iotfaults_alarm.deviceType_id"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_alarm.type_id"
            + " GROUP BY deviceType_id, type_id;")
        rows = cursor.fetchall()
        
        graphData = Graphdata(0)
        graphData.load(rows)
        
        data = {}
        data["categories"] = graphData.get_categories()
        data["series"] = graphData.get_series()
    return data    
    
# Get data structure with information to build Device per Fault Types Graph
def getDataDeviceFaults():
    with connection.cursor() as cursor:
        cursor.execute("SELECT device, DATE(time), count(0)"
            + " FROM iotfaults_alarm"
            + " GROUP BY device, DATE(time);")
        rows = cursor.fetchall()
        
        graphData = Graphdata(0)
        graphData.load(rows)
        
        data = {}
        data["categories"] = graphData.get_categories()
        data["series"] = graphData.get_series()
    return data    

# Create your views here.
def index(request):
    alarms = Alarm.objects.all()[:10]
    context = {
        'title': 'Latest alarms',
        'alarms': alarms,
        'dataGraphPieFaultTypes': json.dumps(getDataFaultTypes()) ,
        'dataGraphPieDeviceTypes': json.dumps(getDataFaultDeviceTypes()) ,
        'dataGraphBarFaultTypesDevice': json.dumps(getDataDeviceFaultTypes()) ,
        'dataGraphLineDeviceFaults': json.dumps(getDataDeviceFaults()) ,
    }
    return render(request, 'iotfaults/index.html', context)


def details(request, id):
    alarm = Alarm.objects.get(id=id) 
    context = {
        'alarm': alarm,
    }
    return render(request, 'iotfaults/details.html', context)