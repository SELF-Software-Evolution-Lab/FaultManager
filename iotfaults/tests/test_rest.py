import json

from rest_framework import status
from rest_framework.test import APITestCase
from iotfaults.models import Type, Component, Event

class TypeRestTest(APITestCase) :

    def setUp(self):
        Type.objects.create(name="Node Failure")
        Type.objects.create(name="Out of Range")
        Type.objects.create(name="Event Loss")
        Type.objects.create(name="State Mismatch")
        Type.objects.create(name="Command Error")
        Component.objects.create(name="Component 1", url="http://iot.net/33c9a023d3cfaef3", latitude="4.57364500", longitude="-74.08455000")
        Component.objects.create(name="Component 2", url="http://iot.net/14cce53d2d3724f8", latitude="4.57238100", longitude="-74.08298300")
        Component.objects.create(name="Component 3", url="http://iot.net/c7ed445e2935e688", latitude="4.57553400", longitude="-74.08596700")
        Component.objects.create(name="Component 4", url="http://iot.net/04ea3e9fe03095c0", latitude="4.57410100", longitude="-74.08334200")
        Component.objects.create(name="Component 5", url="http://iot.net/ccd7bb2392f7b7e1", latitude="4.57421800", longitude="-74.08677100")

    def do_test_get_type(self):
        response = self.client.get('/iotfaults/api/types/1/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status get type')
        self.assertEqual(1, data['id'], 'Type key comparison')
        self.assertEqual('Node Failure', data['name'], 'Type name comparison')

    def do_test_get_types(self):
        response = self.client.get('/iotfaults/api/types/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status get types')
        self.assertEqual(data['count'], 5, 'Types Quantity')

    def do_test_get_component(self):
        response = self.client.get('/iotfaults/api/components/1/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status get component')
        self.assertEqual(1, data['id'], 'Component key comparison')
        self.assertEqual('Component 1', data['name'], 'Component name comparison')

    def do_test_get_components(self):
        response = self.client.get('/iotfaults/api/components/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status get components')
        self.assertEqual(data['count'], 5, 'Components Quantity')

    def do_test_create_event(self):
        dict = {'component_id': '1', 'type_id': '1'}
        response = self.client.post('/iotfaults/api/events/', json.dumps(dict), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Status post event')
        self.assertEqual('1', data['id'], 'Event key comparison')

    def do_test_get_event(self):
        response = self.client.get('/iotfaults/api/events/1/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status get event')
        self.assertEqual(1, data['id'], 'Event key comparison')

    def do_test_get_events(self):
        response = self.client.get('/iotfaults/api/events/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Status get events')
        self.assertEqual(data['count'], 1, 'Events Quantity')

    def test_view(self):
        self.do_test_get_type()
        self.do_test_get_types()
        self.do_test_get_component()
        self.do_test_get_components()
        self.do_test_create_event()

