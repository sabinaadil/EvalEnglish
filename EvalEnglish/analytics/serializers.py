from rest_framework import serializers
from .models import ActivityMetrics

class ActivityMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityMetrics
        fields = ('id', 'user', 'module', 'activity_date', 'tasks_completed', 'average_score')
        read_only_fields = ('id',)
