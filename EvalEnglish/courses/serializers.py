from rest_framework import serializers
from .models import Course, Module, Lesson, CourseParticipant
from users.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'teacher', 'created_at', 'updated_at')
        read_only_fields = ('id', 'teacher', 'created_at', 'updated_at')

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'course', 'title', 'description', 'order', 'created_at', 'due_date')
        read_only_fields = ('id', 'created_at')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'module', 'title', 'content', 'content_url', 'order', 'deadline', 'time_limit', 'created_at')
        read_only_fields = ('id', 'created_at')

class CourseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = ('id', 'course', 'participant', 'enrolled_at', 'progress')
        read_only_fields = ('id', 'enrolled_at')