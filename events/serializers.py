from .models import Event
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class EventSerializer(serializers.Serializer):
    class Meta(object):
        model = Event
        fields = '__all__'