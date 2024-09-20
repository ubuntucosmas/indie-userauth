from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

# Create your views here.

from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

# class EventListCreateView(generics.ListCreateAPIView):
#     queryset = Event.objects.all().order_by('-created_at')  # Order by latest created
#     serializer_class = EventSerializer

#     def get_serializer_context(self):
#         """Provide the request object to the serializer."""
#         return {'request': self.request}
    
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-created_at')  # Latest event first
    serializer_class = EventSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,  # Passing the request to the serializer
        })
        return context