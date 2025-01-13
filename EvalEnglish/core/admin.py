from django.contrib import admin
from .models import EventLog

@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'description', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('user__email', 'description')
    ordering = ('-created_at',)
