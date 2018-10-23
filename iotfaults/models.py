from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.forms import ModelForm
import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

## Classes

class Type(models.Model):
    """Defines a fault type"""
    name = models.CharField(max_length=100, null=False)
    def __str__(self): 
        return str(self.id) + ' - ' + self.name

class Component(models.Model):
    """Defines a fault type"""
    name = models.CharField(max_length=100, null=False)
    url = models.CharField(max_length=200, null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=False)
    def __str__(self): 
        return str(self.id) + ' - ' + self.name

class Event(models.Model):
    """Defines a fault event"""
    component = models.ForeignKey(Component, related_name='events', 
        on_delete=models.CASCADE)   
    type = models.ForeignKey(Type, related_name='events', 
        on_delete=models.CASCADE)   
    time = models.DateTimeField(default=datetime.now, null=False, blank=True)
    def __str__(self): 
        return str(self.id) + ' - ' + self.type.name + ', ' + self.component.name + ' on ' + self.time.strftime("%Y-%m-%d %H:%M:%S")
        
    # def save(self, *args, **kwargs):
    #     if self.time is None:
    #         self.time
    #     super().save(*args, **kwargs)


## Forms

class TypeForm(ModelForm):
    """Form for Type"""
    class Meta:
        model = Type
        fields = ['id', 'name']

class ComponentForm(ModelForm):
    """Form for Component"""
    class Meta:
        model = Component
        fields = ['id', 'name', 'url', 'latitude', 'longitude']
        

## Signals

def tell_client_event_saved():
    """Tell to client that one event was saved to Database"""
    print('Sending from Model to Websocket')
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('event_changes', {
                'type': 'event_message',
                'message': 'savedEvent'
            })

@receiver(post_save, sender=Event)
def post_save_handler(sender, **kwargs):
    """
    Get signal for post save for Model Event to tell to client 
    that an even was saved he on commit is due
    """
    transaction.on_commit(tell_client_event_saved)
