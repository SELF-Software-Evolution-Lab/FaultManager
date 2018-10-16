from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
import json
from django.db import connection
from .utils.graphdata import Graphdata
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import channels.layers
from datetime import datetime
from dateutil.relativedelta import relativedelta
import iotfaults.keys

# Get data structure with information to build Fault Types Graph
def get_data_fault_types(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_event.type_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY type_id;", 
            [
                start_date.strftime('%Y-%m-%d %H:%M'),
                end_date.strftime('%Y-%m-%d %H:%M')
            ])
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({"name": row[0], "y": row[1]})

    return data   
    
# Get data structure with information to build Component per Fault Types Graph
def get_data_struc_url_faults(start_date, end_date, str_date_group):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_component.name, DATE_FORMAT(time, %s), count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_component"
            + " ON iotfaults_component.id = iotfaults_event.component_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_component.name, DATE_FORMAT(time, %s);", 
            [
                str_date_group,
                start_date.strftime('%Y-%m-%d %H:%M'),
                end_date.strftime('%Y-%m-%d %H:%M'),
                str_date_group
            ])
        rows = cursor.fetchall()
        
        graphData = Graphdata(0)
        graphData.load(rows)
        
        data = {}
        data["categories"] = graphData.get_categories()
        data["series"] = graphData.get_series()
    return data    
    

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_data_component_faults_start_end(start_date, end_date):
    diff = end_date - start_date
    str_date_group = '%Y'
    if diff.days <= 365:
        str_date_group += '-%m'
    if diff.days <= 31:
        str_date_group += '-%d'
    if diff.days <= 1:
        str_date_group += ' %Hh'
        if diff.seconds <= 3600:
            str_date_group += '%im'
        if diff.seconds <= 60:
            str_date_group += ':%ss'
    return get_data_struc_url_faults(start_date, end_date, str_date_group)   

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_data_component_faults_quantity_interval(quantity, date_type):
    end_date = datetime.now()
    
    # Default to Years
    str_date_group = '%Y'
    start_date = end_date + relativedelta(years=-quantity)
    if date_type == "Months":
        str_date_group = '%Y-%m'
        start_date = end_date + relativedelta(months=-quantity)
    elif date_type == "Weeks":
        str_date_group = '%Y-%u'
        start_date = end_date + relativedelta(weeks=-quantity)
    elif date_type == "Days":
        str_date_group = '%Y-%m-%d'
        start_date = end_date + relativedelta(days=-quantity)
    elif date_type == "Hours":
        str_date_group = '%Y-%m-%d %Hh'
        start_date = end_date + relativedelta(hours=-quantity)
    elif date_type == "Minutes":
        str_date_group = '%Y-%m-%d %Hh%im'
        start_date = end_date + relativedelta(minutes=-quantity)
    elif date_type == "Seconds":
        str_date_group = '%Y-%m-%d %Hh%im:%ss'
        start_date = end_date + relativedelta(seconds=-quantity)
    return get_data_struc_url_faults(start_date, end_date, str_date_group)   

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_data_component_location_quantity_interval(quantity, date_type):
    end_date = datetime.now()
    
    # Default to Years
    start_date = end_date + relativedelta(years=-quantity)
    if date_type == "Months":
        start_date = end_date + relativedelta(months=-quantity)
    elif date_type == "Weeks":
        start_date = end_date + relativedelta(weeks=-quantity)
    elif date_type == "Days":
        start_date = end_date + relativedelta(days=-quantity)
    elif date_type == "Hours":
        start_date = end_date + relativedelta(hours=-quantity)
    elif date_type == "Minutes":
        start_date = end_date + relativedelta(minutes=-quantity)
    elif date_type == "Seconds":
        start_date = end_date + relativedelta(seconds=-quantity)
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_component.id,"
            + " iotfaults_component.name,"
            + " iotfaults_component.url,"
            + " iotfaults_component.latitude,"
            + " iotfaults_component.longitude,"
            + " count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_component"
            + " ON iotfaults_component.id = iotfaults_event.component_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_component.id,"
            + " iotfaults_component.name,"
            + " iotfaults_component.url,"
            + " iotfaults_component.latitude,"
            + " iotfaults_component.longitude;", 
            [
                start_date.strftime('%Y-%m-%d %H:%M'),
                end_date.strftime('%Y-%m-%d %H:%M'),
            ])
        rows = cursor.fetchall()
        
        data = []
        for tuple in rows:
            obj = {}
            obj["id"] = str(tuple[0])
            obj["name"] = str(tuple[1])
            obj["url"] = str(tuple[2])
            obj["latitude"] = str(tuple[3])
            obj["longitude"] = str(tuple[4])
            obj["faults"] = tuple[5]
            data.append(obj)
    return data    

# View for dinamic graphics
def real_time(request):
    #events = Event.objects.all()[:10]
    context = {
        'title': 'Dashboard - Dynamic',
        'google_maps_key': iotfaults.keys.GOOGLE_MAPS_PRIVATE_KEY,
    }
    return render(request, 'iotfaults/realtime.html', context)

# View for static graphics
def analytics(request):
    #events = Event.objects.all()[:10]
    context = {
        'title': 'Dashboard - Static',
    }
    
    #print('Enviando al chat')
    #channel_layer = channels.layers.get_channel_layer()
    #from asgiref.sync import async_to_sync
    #async_to_sync(channel_layer.group_send)('chat_lobby', {
    #            'type': 'chat_message',
    #            'message': 'Prueba desde static'
    #        })

    return render(request, 'iotfaults/analytics.html', context)

def details(request, id):
    event = Event.objects.get(id=id) 
    context = {
        'event': event,
    }
    return render(request, 'iotfaults/details.html', context)
    
def jsonDataFaultTypes(request, str_start_date, str_end_date):
    start_date = datetime.strptime(str_start_date, '%Y%m%d%H%M')
    end_date = datetime.strptime(str_end_date, '%Y%m%d%H%M')
    data = get_data_fault_types(start_date, end_date)
    return JsonResponse(data, safe=False)
    
def component_faults_start_end(request, str_start_date, str_end_date):
    start_date = datetime.strptime(str_start_date, '%Y%m%d%H%M')
    end_date = datetime.strptime(str_end_date, '%Y%m%d%H%M')
    data = get_data_component_faults_start_end(start_date, end_date)
    return JsonResponse(data, safe=False)    
    
def component_faults_last_interval(request, str_quantity, str_date_type):
    data = get_data_component_faults_quantity_interval(int(str_quantity), str_date_type)
    return JsonResponse(data, safe=False)    
    
def component_location_last_interval(request, str_quantity, str_date_type):
    data = get_data_component_location_quantity_interval(int(str_quantity), str_date_type)
    return JsonResponse(data, safe=False)    
    
    
####### EXAMPLE WebSokects with Channels    

def index_chat(request):
    return render(request, 'iotfaults/index_chat.html', {})
    
def room(request, room_name):
    return render(request, 'iotfaults/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })    