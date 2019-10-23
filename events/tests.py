from django.test import TestCase, APITestCase
from .models import Event
from .serializers import EventSerializer
from rest_framework.test import APIClient

# TODO: Complete these tests

class EventViewTest(APITestCase):

  def setUp(self):
    self.client = APIClient()
    self.event = Event.objects.Create(
      name="Test"
    )

  def test_event_serialization(self):
    data = EventSerializer(instance=self.event).data
    self.response = self.client.get(
            reverse('events'),
            format="json")
    response_data = json.loads(response.content)