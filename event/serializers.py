from .models import Event
from rest_framework import serializers



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'desc', 'venue','image','date','ticketLink']