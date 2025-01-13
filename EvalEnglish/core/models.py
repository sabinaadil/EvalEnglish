from django.db import models
import uuid
from users.models import User

class EventLog(models.Model):
    EVENT_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('data_change', 'Data Change'),
        ('task_complete', 'Task Complete'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='event_logs'
    )
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Event Log"
        verbose_name_plural = "Event Logs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} event by {self.user.email if self.user else 'System'}"
