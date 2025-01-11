# from django.db import models
# from django.contrib.auth import get_user_model
# from courses.models import Course, Module
#
# User = get_user_model()
#
# class ActivityMetrics(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_metrics')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='activity_metrics')
#     module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_metrics')
#     date = models.DateField()  # Дата активности
#     time_spent = models.PositiveIntegerField()  # Время, потраченное за день (в минутах)
#     tasks_completed = models.PositiveIntegerField()  # Количество выполненных заданий
#     average_score = models.FloatField()  # Средний балл за день
#
#     class Meta:
#         verbose_name = "Activity Metric"
#         verbose_name_plural = "Activity Metrics"
#         ordering = ['-date']
#
#     def __str__(self):
#         return f"{self.user} - {self.course} - {self.date}"
