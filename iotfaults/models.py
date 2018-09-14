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

# Class FaultDeviceType: Defnes a fault device type
class DeviceType(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __unicode__(self): 
        return str(self.id) + ' - ' + self.name
    
    # Class FaultDeviceType: Defnes a fault device type
class Alarm(models.Model):
    device = models.CharField(max_length=100, null=False)
    deviceType = models.ForeignKey(DeviceType, related_name='alarms', null=False, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, related_name='alarms', null=False, on_delete=models.CASCADE)   
    time = models.DateTimeField(default=datetime.now, null=False, blank=True)
    def __unicode__(self): 
        return str(self.id) + ' - ' + self.type.name + ', ' + self.deviceType.name + ' ' + self.device + ' on ' + self.time.strftime("%Y-%m-%d %H:%M:%S")

class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['id', 'name']
