from rest_framework import serializers
from .models import EventLog

class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = ('id', 'user', 'event_type', 'description', 'created_at')
        read_only_fields = ('id', 'created_at')
