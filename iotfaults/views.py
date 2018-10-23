from django.shortcuts import render
from django.http import HttpResponse
from .models import Type, Component, Event
import json
from django.db import connection
from .utils.graphdata import Graphdata
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from datetime import datetime
from dateutil.relativedelta import relativedelta
import iotfaults.keys
from rest_framework import viewsets, mixins
from .serializers import TypeSerializer, ComponentSerializer, EventSerializer

# PRIVATE

# Get data structure with information to build Fault Types Graph
def get_db_data_struc_fault_types_count_between(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_event.type_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY type_id" 
            + " LIMIT 100;", 
            [
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            ])
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({"name": row[0], "y": row[1]})

    return data   
    
# Get data structure with information to build Component per Fault Types Graph
def get_db_data_struc_components_date_group_count_between(start_date, end_date, str_date_group):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_component.name, DATE_FORMAT(time, %s), count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_component"
            + " ON iotfaults_component.id = iotfaults_event.component_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_component.name, DATE_FORMAT(time, %s)" 
            + " ORDER BY iotfaults_event.time" 
            + " LIMIT 100;", 
            [
                str_date_group,
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
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
def get_data_components_count_between(start_date, end_date):
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
    return get_db_data_struc_components_date_group_count_between(start_date, end_date, str_date_group)   

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_data_components_count_last(quantity, date_type):
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
    return get_db_data_struc_components_date_group_count_between(start_date, end_date, str_date_group)   

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_db_data_struc_components_detail_count_last(quantity, date_type):
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
            + " iotfaults_component.longitude" 
            + " LIMIT 100;", 
            [
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
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

# RENDERS

# Index view
def index(request):
    context = {
        'title': 'Index',
    }
    return render(request, 'iotfaults/index.html', context)

# View for dinamic graphics
def real_time(request):
    #events = Event.objects.all()[:10]
    context = {
        'title': 'Dashboard - Real Time',
        'google_maps_key': iotfaults.keys.GOOGLE_MAPS_PRIVATE_KEY,
    }
    return render(request, 'iotfaults/realtime.html', context)

# View for static graphics
def analytics(request):
    #events = Event.objects.all()[:10]
    context = {
        'title': 'Dashboard - Analytics',
    }

    return render(request, 'iotfaults/analytics.html', context)

# Fault Detail View
def event_detail(request, id):
    event = Event.objects.get(id=id) 
    context = {
        'event': event,
    }
    return render(request, 'iotfaults/eventdetail.html', context)
    
# Node Failure Event Simulator View
def node_failure_simulator(request):
    context = {
        'title': 'Node Failure Simulator',
        'event_type_id': 1,
        'max_events_in_table': 50,
        'default_automatic_seconds': 10,
    }
    return render(request, 'iotfaults/eventsimulator.html', context)

# Node Failure Event Simulator View
def out_of_range_simulator(request):
    context = {
        'title': 'Out of Range Simulator',
        'event_type_id': 2,
        'max_events_in_table': 50,
        'default_automatic_seconds': 10,
    }
    return render(request, 'iotfaults/eventsimulator.html', context)

# JSON GRAPH DATA  

# Return Json data about Fault Types
def json_fault_types_count_between(request, str_start_date, str_end_date):
    start_date = datetime.strptime(str_start_date, '%Y%m%d%H%M')
    end_date = datetime.strptime(str_end_date, '%Y%m%d%H%M')
    data = get_db_data_struc_fault_types_count_between(start_date, end_date)
    return JsonResponse(data, safe=False)
    
# Return Json data about Component faults between start date and end date
def json_components_count_between(request, str_start_date, str_end_date):
    start_date = datetime.strptime(str_start_date, '%Y%m%d%H%M')
    end_date = datetime.strptime(str_end_date, '%Y%m%d%H%M')
    data = get_data_components_count_between(start_date, end_date)
    return JsonResponse(data, safe=False)    
    
# Return Json data about Component faults between last interval 
# determined by quantity and date type 
# e.g. Quantity: 24 Date Type: Days is last 24 days
def json_components_count_last(request, str_quantity, str_date_type):
    data = get_data_components_count_last(int(str_quantity), str_date_type)
    return JsonResponse(data, safe=False)    
    
# Return Json data about Component faults for Map between last interval 
# determined by quantity and date type 
# e.g. Quantity: 24 Date Type: Days is last 24 days
def json_components_detail_count_last(request, str_quantity, str_date_type):
    data = get_db_data_struc_components_detail_count_last(int(str_quantity), str_date_type)
    return JsonResponse(data, safe=False)   
    
# REST

class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    
class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve` and `create` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass

class EventViewSet(CreateRetrieveViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer