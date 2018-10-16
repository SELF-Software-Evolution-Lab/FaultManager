"""django_iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # General index. Real Time Graphics
    url(r'^$', views.real_time, name='real_time'),
    
    # Show all data in Events table
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    
    # Show Static Graphs
    url(r'^analytics$', views.analytics, name='analytics'),
    
    # Get data of Fault types since start date to end date
    url(r'^fault-types/start/(?P<str_start_date>[^/]+)/end/(?P<str_end_date>[^/]+)$', views.jsonDataFaultTypes, name='datafaulttypes'),

    # Get data of Components with Faults since start date to end date
    url(r'^component-faults/start/(?P<str_start_date>[^/]+)/end/(?P<str_end_date>[^/]+)$', views.component_faults_start_end, name='component_faults_start_end'),
    
    # Get data of Components with Faults last quantity of time
    url(r'^component-faults/quantity/(?P<str_quantity>[^/]+)/date-type/(?P<str_date_type>[^/]+)$', views.component_faults_last_interval, name='component_faults_last_interval'),
    
    # Get data of Components with Location with Faults last quantity of time
    url(r'^component-location/quantity/(?P<str_quantity>[^/]+)/date-type/(?P<str_date_type>[^/]+)$', views.component_location_last_interval, name='component_location_last_interval'),
    
    
    #### EXAMple Channels
    # Index Chat
    url(r'^indexchat/$', views.index_chat, name='index_chat'),
    #url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
