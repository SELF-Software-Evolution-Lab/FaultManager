from django.test import TestCase
from iotfaults.models import Type, Component, Event
from django.core.exceptions import ObjectDoesNotExist

class TypeTestCase(TestCase):
    
    def do_test_create_type(self):
        obj = Type.objects.create(name="Node Failure")
        self.assertEqual(obj.name, 'Node Failure')

    def do_test_modify_type(self):
        obj = Type.objects.get(name="Node Failure")
        obj.name = 'Other Failure'
        obj.save()
        obj = Type.objects.get(name="Other Failure")
        obj.name = 'Node Failure'
        obj.save()
        
    def do_test_delete_type(self):
        obj = Type.objects.get(name="Node Failure")
        obj.delete()
        try:
            Type.objects.get(name="Node Failure")
            self.fail("Not deleted")
        except ObjectDoesNotExist:
            pass

    def do_test_type_model(self):
        self.do_test_create_type()
        self.do_test_modify_type()
        self.do_test_delete_type()

    def do_test_create_component(self):
        obj = Component.objects.create(name="Component 1", url="http://iot.net/33c9a023d3cfaef3", latitude="4.57364500", longitude="-74.08455000")
        self.assertEqual(obj.name, 'Component 1')

    def do_test_modify_component(self):
        obj = Component.objects.get(name="Component 1")
        obj.name = 'Other Component'
        obj.save()
        obj = Component.objects.get(name="Other Component")
        obj.name = 'Component 1'
        obj.save()
        
    def do_test_delete_component(self):
        obj = Component.objects.get(name="Component 1")
        obj.delete()
        try:
            Component.objects.get(name="Component 1")
            self.fail("Not deleted")
        except ObjectDoesNotExist:
            pass

    def do_test_component_model(self):
        self.do_test_create_component()
        self.do_test_modify_component()
        self.do_test_delete_component()

    def do_test_create_event(self):
        type = Type.objects.create(name="Node Failure")
        component = Component.objects.create(name="Component 1", url="http://iot.net/33c9a023d3cfaef3", latitude="4.57364500", longitude="-74.08455000")
        event = Event.objects.create(component=component, type=type)
        self.event_id = event.id
        Event.objects.get(pk=self.event_id)

    def do_test_modify_event(self):
        type = Type.objects.create(name="Other Failure")
        obj = Event.objects.get(pk=self.event_id)
        obj.type_id = type.id
        obj.save()
        obj = Event.objects.get(pk=self.event_id)
        self.assertEqual(obj.type_id, type.id)

    def do_test_delete_event(self):
        obj = Event.objects.get(pk=self.event_id)
        obj.delete()
        try:
            Event.objects.get(pk=self.event_id)
            self.fail("Not deleted")
        except ObjectDoesNotExist:
            pass

    def do_test_event_model(self):
        self.do_test_create_event()
        self.do_test_modify_event()
        self.do_test_delete_event()

    def test_models(self):
        self.do_test_type_model()
        self.do_test_component_model()
        self.do_test_event_model()