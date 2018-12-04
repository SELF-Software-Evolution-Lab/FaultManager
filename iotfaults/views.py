from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from django.core import serializers
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.safestring import mark_safe
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
import iotfaults.keys
import json
from .models import Type, Component, Event
from .serializers import TypeSerializer, ComponentSerializer, EventSerializer
from .utils.graphdata import Graphdata

# PRIVATE

# Get data structure with information to build Fault Types Graph
def get_db_data_struc_types_count_between(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.id, iotfaults_type.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_event.type_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_type.id, iotfaults_type.name" 
            + " LIMIT 100;", 
            [
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            ])
        rows = cursor.fetchall()
        points_data = []
        for row in rows:
            points_data.append({"typeId": row[0], "name": row[1], "y": row[2]})
            
        metadata = {}
        metadata["startDate"] = start_date
        metadata["endDate"] = end_date
        
        data = {}
        data["pointsData"] = points_data
        data["metadata"] = metadata

    return data   
    
# Get data structure with information to build Fault Types Graph
def get_db_data_struc_component_types_count_between(component_id, start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_type.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_type"
            + " ON iotfaults_type.id = iotfaults_event.type_id"
            + " WHERE iotfaults_event.component_id = %s"
            + " AND iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_event.type_id" 
            + " LIMIT 100;", 
            [
                component_id,
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            ])
        rows = cursor.fetchall()
        points_data = []
        for row in rows:
            points_data.append({"name": row[0], "y": row[1]})
            
        metadata = {}
        metadata["startDate"] = start_date
        metadata["endDate"] = end_date
        
        data = {}
        data["pointsData"] = points_data
        data["metadata"] = metadata

    return data   
    
# Get data structure with information to build Component per Fault Types Graph
def get_db_data_struc_components_count_between(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_component.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_component"
            + " ON iotfaults_component.id = iotfaults_event.component_id"
            + " WHERE iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_event.component_id" 
            + " LIMIT 100;", 
            [
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            ])
        rows = cursor.fetchall()
        points_data = []
        for row in rows:
            points_data.append({"name": row[0], "y": row[1]})
            
        metadata = {}
        metadata["startDate"] = start_date
        metadata["endDate"] = end_date
        
        data = {}
        data["pointsData"] = points_data
        data["metadata"] = metadata

    return data    

# Get data structure with information to build Component per Fault Types Graph
def get_db_data_struc_type_components_count_between(type_id, start_date, end_date):
    print("Valor de type_id " + type_id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT iotfaults_component.name, count(0)"
            + " FROM iotfaults_event"
            + " INNER JOIN iotfaults_component"
            + " ON iotfaults_component.id = iotfaults_event.component_id"
            + " WHERE iotfaults_event.type_id = %s"
            + " AND iotfaults_event.time >= %s"
            + " AND iotfaults_event.time <= %s"
            + " GROUP BY iotfaults_event.component_id" 
            + " LIMIT 100;", 
            [
                type_id,
                start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                end_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            ])
        rows = cursor.fetchall()
        points_data = []
        for row in rows:
            points_data.append({"name": row[0], "y": row[1]})
            
        metadata = {}
        metadata["startDate"] = start_date
        metadata["endDate"] = end_date
        
        data = {}
        data["pointsData"] = points_data
        data["metadata"] = metadata

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
        
        metadata = {}
        metadata["startDate"] = start_date
        metadata["endDate"] = end_date
        
        data = {}
        data["categories"] = graphData.get_categories()
        data["series"] = graphData.get_series()
        data["metadata"] = metadata
    return data    
    

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_data_components_date_group_count_between(start_date, end_date):
    diff = end_date - start_date
    str_date_group = '%Y'
    if diff.days <= 365:
        str_date_group += '-%m'
    if diff.days <= 31:
        str_date_group += '-%d'
    if diff.days <= 1:
        str_date_group += ' %H'
        if diff.seconds <= 3600:
            str_date_group += ':%i'
        if diff.seconds <= 60:
            str_date_group += ':%s'
    return get_db_data_struc_components_date_group_count_between(start_date, end_date, str_date_group)   

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_data_components_date_group_count_last(quantity, date_type):
    end_date = timezone.now()
    
    # Default to Years
    str_date_group = '%Y'
    start_date = end_date + relativedelta(years=-quantity)
    if date_type == "Months":
        str_date_group = '%Y-%m'
        start_date = end_date + relativedelta(months=-quantity)
    elif date_type == "Weeks":
        str_date_group = '%Y-%w'
        start_date = end_date + relativedelta(weeks=-quantity)
    elif date_type == "Days":
        str_date_group = '%Y-%m-%d'
        start_date = end_date + relativedelta(days=-quantity)
    elif date_type == "Hours":
        str_date_group = '%Y-%m-%d %Hh'
        start_date = end_date + relativedelta(hours=-quantity)
    elif date_type == "Minutes":
        str_date_group = '%Y-%m-%d %H:%i'
        start_date = end_date + relativedelta(minutes=-quantity)
    elif date_type == "Seconds":
        str_date_group = '%Y-%m-%d %H:%i:%s'
        start_date = end_date + relativedelta(seconds=-quantity)
    return get_db_data_struc_components_date_group_count_between(start_date, end_date, str_date_group)   

# Get data structure with information to build Component per Fault Types Graph 
# between start date and end date
def get_db_data_struc_components_detail_count_last(quantity, date_type):
    end_date = timezone.now()
    
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
            + " count(0) event_count"
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

        points_data = []
        for tuple in rows:
            obj = {}
            obj["id"] = str(tuple[0])
            obj["name"] = str(tuple[1])
            obj["url"] = str(tuple[2])
            obj["latitude"] = str(tuple[3])
            obj["longitude"] = str(tuple[4])
            obj["event_count"] = tuple[5]
            points_data.append(obj)
            
        metadata = {}
        metadata["startDate"] = start_date
        metadata["endDate"] = end_date
        
        data = {}
        data["pointsData"] = points_data
        data["metadata"] = metadata

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

# REST

class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows types to be viewed.
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    # Return Json data about Type event count between start date and end date
    @action(detail=False, url_path='event_count/start/(?P<start_date>[^/]+)/end/(?P<end_date>[^/]+)')
    def event_count_between(self, request, *args, **kwargs):
        start_date = parse(kwargs['start_date'])
        end_date = parse(kwargs['end_date'])
        data = get_db_data_struc_types_count_between(start_date, end_date)
        return Response(data)

    # Return Json data about Type event count between start date and end date
    @action(detail=False, url_path='event_count/component/(?P<component_id>[^/]+)/start/(?P<start_date>[^/]+)/end/(?P<end_date>[^/]+)')
    def component_event_count_between(self, request, *args, **kwargs):
        component_id = kwargs['component_id']
        start_date = parse(kwargs['start_date'])
        end_date = parse(kwargs['end_date'])
        data = get_db_data_struc_component_types_count_between(component_id, start_date, end_date)
        return Response(data)


class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows components to be viewed.

    list:
    Return a list of all the existing components.

    read:
    Return an existing component by id.
    
    event_count_for_map:
    Return a list of components with event count for a map between quantity 
    and date_type.
    
    event_count_last:
    Return a list of components with event count for a map between quantity 
    and date_type.
    
    event_count_between:
    Return a list of components with event count for a map between quantity 
    and date_type.
    
    """
    
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    
    # Return Json data about Component Event Count for Map between last interval 
    # determined by quantity and date type 
    # e.g. Quantity: 24 Date Type: Days is last 24 days
    @action(detail=False, url_path='event_count_for_map/quantity/(?P<quantity>[^/]+)/date-type/(?P<date_type>[^/]+)')
    def event_count_for_map(self, request, *args, **kwargs):
        quantity = int(kwargs['quantity'])
        date_type = kwargs['date_type']
        data = get_db_data_struc_components_detail_count_last(quantity, date_type)
        return Response(data)
        
    # Return Json data about Component event count between last interval 
    # determined by quantity and date type 
    # e.g. Quantity: 24 Date Type: Days is last 24 days
    @action(detail=False, url_path='event_date_group_count/quantity/(?P<quantity>[^/]+)/date-type/(?P<date_type>[^/]+)')
    def event_date_group_count_last(self, request, *args, **kwargs):
        quantity = int(kwargs['quantity'])
        date_type = kwargs['date_type']
        data = get_data_components_date_group_count_last(quantity, date_type)
        return Response(data)
        
    # Return Json data about Component event count between start date and end date
    @action(detail=False, url_path='event_date_group_count/start/(?P<start_date>[^/]+)/end/(?P<end_date>[^/]+)')
    def event_date_group_count_between(self, request, *args, **kwargs):
        start_date = parse(kwargs['start_date'])
        end_date = parse(kwargs['end_date'])
        data = get_data_components_date_group_count_between(start_date, end_date)
        return Response(data)
        
    # Return Json data about Type event count between start date and end date
    @action(detail=False, url_path='event_count/start/(?P<start_date>[^/]+)/end/(?P<end_date>[^/]+)')
    def event_count_between(self, request, *args, **kwargs):
        start_date = parse(kwargs['start_date'])
        end_date = parse(kwargs['end_date'])
        data = get_db_data_struc_components_count_between(start_date, end_date)
        return Response(data)

    # Return Json data about Type event count between start date and end date
    @action(detail=False, url_path='event_count/type/(?P<type_id>[^/]+)/start/(?P<start_date>[^/]+)/end/(?P<end_date>[^/]+)')
    def type_event_count_between(self, request, *args, **kwargs):
        type_id = kwargs['type_id']
        start_date = parse(kwargs['start_date'])
        end_date = parse(kwargs['end_date'])
        data = get_db_data_struc_type_components_count_between(type_id, start_date, end_date)
        return Response(data)
    
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
    """
    API endpoint that allows events to be viewed.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    # Return Json data about Last quantity of Events  
    # e.g. Quantity: 24 Date Type: Days is last 24 days
    @action(detail=False, url_path='last/(?P<quantity>[^/]+)')
    def last_quantity(self, request, *args, **kwargs):
        quantity = 1000
        if 'quantity' in kwargs:
            quantity = int(kwargs['quantity'])
        sliceObj = slice(0, quantity)
        events = Event.objects.all().order_by('-time')[sliceObj]

        # page = self.paginate_queryset(events)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    # Return Json data about Last Events  
    # e.g. Quantity: 24 Date Type: Days is last 24 days
    @action(detail=False)
    def last(self, request, *args, **kwargs):
        return self.last_quantity(self, request, args, kwargs)

    # Return Json data about Events between start date and end date
    @action(detail=False, url_path='start/(?P<start_date>[^/]+)/end/(?P<end_date>[^/]+)')
    def between(self, request, *args, **kwargs):
        start_date = parse(kwargs['start_date'])
        end_date = parse(kwargs['end_date'])
        queryset = Event.objects.filter(time__gte=start_date).filter(time__lte=end_date)
        
        component = request.GET.get('component', None)
        if component is not None:
            queryset = queryset.filter(component_id=component)

        type = request.GET.get('type', None)
        if type is not None:
            queryset = queryset.filter(type_id=type)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
