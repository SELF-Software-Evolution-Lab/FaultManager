from django.test import TestCase
from .models import Type, Component, Event

class AnimalTestCase(TestCase):
    def setUp(self):
        Type.objects.create(name="Node Failure")
        Type.objects.create(name="Out of Range")
        Type.objects.create(name="Event Loss")
        Type.objects.create(name="State Mismatch")
        Type.objects.create(name="Command Error")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        node = Type.objects.get(name="Node Failure")
        self.assertEqual(node.name, 'Node Failure')
