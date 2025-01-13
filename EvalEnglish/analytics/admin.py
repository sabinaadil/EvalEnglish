from django.contrib import admin
from .models import ActivityMetrics

@admin.register(ActivityMetrics)
class ActivityMetricsAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'activity_date', 'tasks_completed', 'average_score')
    list_filter = ('activity_date', 'module')
    search_fields = ('user__email', 'module__title')
    ordering = ('-activity_date',)
