from rest_framework import serializers
from .models import User, TeacherApplication
from common.serializers import DocumentSerializer

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'avatar', 'role', 'is_teacher', 'is_superuser')
    
    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class TeacherApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = TeacherApplication
        fields = ('id', 'user', 'user_email', 'full_name', 'phone', 'status', 'submitted_at', 'reviewed_at',  'rejection_reason', 'documents')
        read_only_fields = ('id', 'user', 'status', 'submitted_at', 'reviewed_at', 'rejection_reason', 'documents')
