from django.db import models
import uuid
from users.models import User
from courses.models import Course, Module

class ActivityMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity_metrics'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='activity_metrics'
    )
    activity_date = models.DateField()
    tasks_completed = models.PositiveIntegerField()
    average_score = models.FloatField()

    class Meta:
        verbose_name = "Activity Metric"
        verbose_name_plural = "Activity Metrics"
        ordering = ['-activity_date']

    def __str__(self):
        return f"Activity of {self.user.email} on {self.activity_date}"
