from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.forms import ModelForm

# Create your models here.

# Class FaultType: Defnes a fault type
class Type(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __unicode__(self): 
        return str(self.id) + ' - ' + self.name

# Class Event: Defines a fault event
class Event(models.Model):
    url = models.CharField(max_length=100, null=False)
    type = models.ForeignKey(Type, related_name='events', null=False, on_delete=models.CASCADE)   
    time = models.DateTimeField(default=datetime.now, null=False, blank=True)
    def __unicode__(self): 
        return str(self.id) + ' - ' + self.type.name + ', ' + self.url + ' on ' + self.time.strftime("%Y-%m-%d %H:%M:%S")

class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['id', 'name']
