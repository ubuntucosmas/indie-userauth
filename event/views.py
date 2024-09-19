from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

# Create your views here.

# List all events and create new events
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

        # Pass request context for handling image URLs in serializer
    def get_serializer_context(self):
        return {'request': self.request}