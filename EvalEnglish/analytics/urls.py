from django.urls import path
from .api import ActivityMetricsAPIView

urlpatterns = [
    path('activity-metrics/', ActivityMetricsAPIView.as_view(), name='activity-metrics'),
]
