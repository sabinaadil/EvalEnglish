from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'content_type', 'object_id', 'file', 'uploaded_at')
    list_filter = ('content_type', 'uploaded_at')
    search_fields = ('uploaded_by__email', 'description')
