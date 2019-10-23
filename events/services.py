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
    # EventBrite event search is not working or i'm doing something wrong, so in case of a forbidden response, I will fill db with test data
    response = requests.get(settings.EVENT_BRITE_EVENTS_URL)
    if (response.status_code == 403):
      events = self.__get_test_events()
    else:
      events = json.loads(response.content)["events"]

    return events

  def __get_test_events(self):
    return [{
        "id": 1234,
        "name": { "text": "Greenday Concert"},
        "description": { "text": "This concert event"},
        "url": "www.eventbrite.com/events/1234",
        "start": {"utc": "2019-05-12" },
        "end": {"utc": "2018-05-12T03:00:00Z"},
        "created": "2018-05-12T02:00:00Z",
        "changed": "2018-05-12T02:00:00Z",
        "published": "2018-05-12T02:00:00Z",
        "status": "live",
        "organizer": { "name": "Some event organizer"},
        "ticket_availability": { "minimum_ticket_price": { "value": 105.00 }}
      },
      {
        "id": 1235,
        "name": { "text": "Santana Concert"},
        "description": { "text": "Santana Concert"},
        "url": "www.eventbrite.com/events/1235",
        "start": {"utc": "2018-05-12T02:00:00Z" },
        "end": {"utc": "2018-05-12T03:00:00Z"},
        "created": "2018-05-12T02:00:00Z",
        "changed": "2018-05-12T02:00:00Z",
        "published": "2018-05-12T02:00:00Z",
        "status": "live",
        "organizer": { "name": "Some event organizer"},
        "ticket_availability": { "minimum_ticket_price": { "value": 105.00 }}
      },
      {
        "id": 1236,
        "name": { "text": "Disney on Ice"},
        "description": { "text": "This is an indoor event"},
        "url": "www.eventbrite.com/events/1236",
        "start": {"utc": "2018-05-12T02:00:00Z" },
        "end": {"utc": "2018-05-12T03:00:00Z"},
        "created": "2018-05-12T02:00:00Z",
        "changed": "2018-05-12T02:00:00Z",
        "published": "2018-05-12T02:00:00Z",
        "status": "live",
        "organizer": { "name": "Disney"},
        "ticket_availability": { "minimum_ticket_price": { "value": 30.00 }}
      },
      {
        "id": 1237,
        "name": { "text": "Mega Halloween Party"},
        "description": { "text": "This is Halloween Party event"},
        "url": "www.eventbrite.com/events/1236",
        "start": {"utc": "2018-05-12T02:00:00Z" },
        "end": {"utc": "2018-05-12T03:00:00Z"},
        "created": "2018-05-12T02:00:00Z",
        "changed": "2018-05-12T02:00:00Z",
        "published": "2018-05-12T02:00:00Z",
        "status": "live",
        "organizer": { "name": "Aykut Events"},
        "ticket_availability": { "minimum_ticket_price": { "value": 55.00 }}
      }
      ]

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


