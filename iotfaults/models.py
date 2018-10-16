from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.forms import ModelForm

# Create your models here.

# Class FaultType: Defnes a fault type
class Type(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self): 
        return str(self.id) + ' - ' + self.name

# Class FaultType: Defnes a fault type
class Component(models.Model):
    name = models.CharField(max_length=100, null=False)
    url = models.CharField(max_length=200, null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=False)
    def __str__(self): 
        return str(self.id) + ' - ' + self.name

# Class Event: Defines a fault event
class Event(models.Model):
    component = models.ForeignKey(Component, related_name='events', on_delete=models.CASCADE)   
    type = models.ForeignKey(Type, related_name='events', on_delete=models.CASCADE)   
    time = models.DateTimeField(default=datetime.now, null=False, blank=True)
    def __str__(self): 
        return str(self.id) + ' - ' + self.type.name + ', ' + self.component.url + ' on ' + self.time.strftime("%Y-%m-%d %H:%M:%S")

class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['id', 'name']

class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = ['id', 'name', 'url', 'latitude', 'longitude']