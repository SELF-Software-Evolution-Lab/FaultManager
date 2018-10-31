from .models import Type, Component, Event
from rest_framework import serializers

class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name')

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('id', 'name', 'url', 'latitude', 'longitude')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    component_id = serializers.IntegerField()
    component_name = serializers.CharField(source='component.name', read_only=True)
    type_id = serializers.IntegerField()
    type_name = serializers.CharField(source='type.name', read_only=True)
    time = serializers.DateTimeField(required = False)
    class Meta:
        model = Event
        fields = ('id', 'component_id', 'component_name', 'type_id', 'type_name', 'time')