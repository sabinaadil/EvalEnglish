from django.db import models
import uuid
from users.models import User
from courses.models import Course, Module
from django.utils import timezone

class ActivityMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity_metrics'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='activity_metrics',
        null=True
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='activity_metrics',
        null=True
    )
    activity_date = models.DateField(default=timezone.now)
    tasks_completed = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    average_teacher_score = models.FloatField(default=0.0)
    average_model_score = models.FloatField(default=0.0)
    time_spent = models.PositiveIntegerField(default=0)
    avg_attempts = models.FloatField(default=0.0)
    late_submissions = models.PositiveIntegerField(default=0)
    final_efficiency_score = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Activity Metric"
        verbose_name_plural = "Activity Metrics"
        ordering = ['-activity_date']

    def __str__(self):
        return f"Activity of {self.user.email} in {self.course.name} on {self.activity_date}"
