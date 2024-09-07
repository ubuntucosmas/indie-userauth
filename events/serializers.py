from .models import Event
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer






from .models import MpesaTransaction

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    # owner = UserSerializer(many=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'event_venue','event_poster','date']