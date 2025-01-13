from django.contrib import admin
from .models import Course, Module, Lesson, CourseParticipant

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_at', 'updated_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('name', 'teacher__email')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'course__name')
    ordering = ('course', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'deadline', 'time_limit', 'created_at')
    list_filter = ('module', 'deadline')
    search_fields = ('title', 'module__title')
    ordering = ('module', 'order')

@admin.register(CourseParticipant)
class CourseParticipantAdmin(admin.ModelAdmin):
    list_display = ('course', 'participant', 'progress', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('participant__email', 'course__name')
    ordering = ('-enrolled_at',)