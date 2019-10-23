from .models import Event
import requests
import json
from lyte import settings


# TODO: Use dependency injection framework here...saving time and skipping for now

class EventRemoteService(object):
  def get_events(self):
    return []

class EventBriteEventRemoteService(EventRemoteService):

  def get_events(self):
    response = requests.get(settings.EVENT_BRITE_EVENTS_URL)
    return json.loads(response.content)["events"]


class EventService:

  def __init__(self, event_remote_service: EventRemoteService):
    self.event_remote_service = event_remote_service

  def init_db(self):
    Event.objects.all().delete()
    response = self.event_remote_service.get_events()
    for eventResult in response:
      event = Event()
      event.event_id = eventResult["id"]
      event.name = eventResult["name"]["text"]
      event.description = eventResult["description"]["text"]
      event.url = eventResult["url"]
      event.start = eventResult["start"]["utc"]
      event.end = eventResult["end"]["utc"]
      event.created = eventResult["created"]
      event.changed = eventResult["changed"]
      event.published = eventResult["published"]
      event.status = eventResult["status"]
      event.organizer = eventResult["organizer"]["name"]
      event.cost = eventResult["ticket_availability"]["minimum_ticket_price"]["value"]
      event.save()

class EventServiceFactory:

  def create(self):
    return EventService(EventBriteEventRemoteService())


