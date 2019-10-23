from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, JsonResponse
from .services import EventServiceFactory
from .models import Event
from django.core import serializers
from .serializers import EventSerializer


def homePageView(request):
  event_service = EventServiceFactory().create()
  event_service.init_db()
  return HttpResponse(Event.objects.all())
  #return HttpResponse("Hello world!")

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'cost', 'start', 'organizer']

class EventView(APIView):
  def put(self, request, id: int):
    try:
      event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    data = JSONParser().parse(request)
    serializer = EventSerializer(event, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)