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
    # General index. Dynamic Graphics
    url(r'^$', views.index, name='index'),
    
    # Show all data in Events table
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    
    # Show Static Graphs
    url(r'^staticgraphs$', views.staticGraphs, name='staticgraphs'),
    
    # Get data of Fault types
    url(r'^datafaulttypes$', views.jsonDataFaultTypes, name='datafaulttypes'),

    # Get data of Components with Faults
    url(r'^dataurlfaults$', views.jsonDataUrlFaults, name='dataurlfaults'),
    
    
    #### EXAMple Channels
    # Index Chat
    url(r'^indexchat/$', views.index_chat, name='index_chat'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
