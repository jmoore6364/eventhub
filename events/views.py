from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, filters
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

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['name', 'cost', 'start', 'organizer']
    ordering_fields = ['name', 'cost', 'start', 'organizer']