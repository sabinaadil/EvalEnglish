from rest_framework import serializers
from .models import ActivityMetrics


class ActivityMetricsSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ActivityMetrics
        fields = [
            'id', 'user', 'user_email', 'course', 'course_name',
            'activity_date', 'tasks_completed', 'average_score',
            'average_teacher_score', 'average_model_score',
            'time_spent', 'avg_attempts', 'late_submissions',
            'final_efficiency_score'
        ]
        read_only_fields = fields

