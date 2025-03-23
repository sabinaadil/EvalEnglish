from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    model = serializers.SerializerMethodField()
    content_type = serializers.IntegerField(write_only=True)
    object_id = serializers.UUIDField()

    class Meta:
        model = Document
        fields = (
            'id', 'uploaded_by', 'uploaded_by_email',
            'file', 'uploaded_at',
            'model', 'content_type', 'object_id'
        )
        read_only_fields = ('id', 'uploaded_by', 'uploaded_at', 'model')

    def get_model(self, obj):
        return obj.content_type.model if obj.content_type else None

    def create(self, validated_data):
        # Достаём content_type_id и object_id из данных
        content_type_id = validated_data.pop('content_type')
        content_type = ContentType.objects.get(id=content_type_id)
        validated_data['content_type'] = content_type

        return super().create(validated_data)
