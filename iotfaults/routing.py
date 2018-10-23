from django.conf.urls import url

from .consumers import EventConsumer

websocket_urlpatterns = [
    url(r'^ws/iotfaults/event/$', EventConsumer),
]