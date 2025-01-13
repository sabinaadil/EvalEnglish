from .models import User, TeacherApplication
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'get_avatar')

class TeacherApplicationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = TeacherApplication
        fields = ('id', 'user', 'user_email', 'document', 'status', 'submitted_at', 'reviewed_at')
        read_only_fields = ('id', 'user', 'status', 'submitted_at', 'reviewed_at')