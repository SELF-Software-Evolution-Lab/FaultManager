from django.contrib import admin
from .models import Type
from .models import Component
from .models import Event

# Register your models here.
admin.site.register(Type)
admin.site.register(Component)
admin.site.register(Event)