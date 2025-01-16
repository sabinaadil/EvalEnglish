from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    class Meta:
        model = Document
        fields = ('id', 'uploaded_by', 'uploaded_by_email', 'file', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_by', 'uploaded_at')
