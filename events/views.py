from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import EventSerializer
from .models import Event
from rest_framework.generics import CreateAPIView,RetrieveAPIView, GenericAPIView

# Create your views here.
# @api_view(['GET'])
# def event_list(request):
#     events = Event.objects.all()
#     event_data = [{
#         'id': event.id,
#         'nickname':f"{event.event_venue} {event.name}",
#         'name': event.name,
#         'description': event.description,
#         'date': event.date,
#     }for event in events]
#     return Response(event_data)
class EventListView(GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()
        serializer = self.get_serializer(events, many=True)
        return JsonResponse(serializer.data)

class eventCreate(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
class eventRetrieve(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
