from django.contrib import admin
from .models import Type
from .models import Event

# Register your models here.
admin.site.register(Type)
admin.site.register(Event)