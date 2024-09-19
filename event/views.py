from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

# Create your views here.

# List all events and create new events
# class EventListCreateView(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer

#     def get_queryset(self):
#         return Event.objects.all().order_by('-created_at')

#         # Pass request context for handling image URLs in serializer
#     def get_serializer_context(self):
#         return {'request': self.request}
    

from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-created_at')  # Order by latest created
    serializer_class = EventSerializer

    def get_serializer_context(self):
        """Provide the request object to the serializer."""
        return {'request': self.request}