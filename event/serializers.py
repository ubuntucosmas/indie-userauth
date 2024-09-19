from .models import Event
from rest_framework import serializers



class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'name', 'desc', 'venue','image','date','ticketLink']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None