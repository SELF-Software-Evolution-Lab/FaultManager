from django.contrib import admin
from models import Type
from models import DeviceType
from models import Alarm

# Register your models here.
admin.site.register(Type)
admin.site.register(DeviceType)
admin.site.register(Alarm)