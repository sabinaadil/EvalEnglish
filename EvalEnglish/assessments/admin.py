from django.contrib import admin
from .models import QuestionType, Question, AnswerOption, UserAnswer, ModuleAssessment, CourseAssessment
from common.models import Document

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_text', 'module', 'question_type',
        'time_limit', 'max_attempts', 'max_score', 'correct_answer', 'created_at'
    )
    list_filter = ('module', 'question_type', 'created_at')
    search_fields = ('question_text', 'module__title', 'correct_answer')
    ordering = ('-created_at',)

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('answer_text', 'question__question_text')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'question', 'attempt_number', 'time_spent',
        'is_correct', 'teacher_score', 'model_score', 'final_score', 'score',
        'submitted_at', 'is_late'
    )
    list_filter = ('is_correct', 'is_late', 'submitted_at')
    search_fields = ('user__email', 'question__question_text')
    ordering = ('-submitted_at',)

@admin.register(ModuleAssessment)
class ModuleAssessmentAdmin(admin.ModelAdmin):
    list_display = ('module', 'user', 'score', 'max_score', 'completed_at')
    list_filter = ('module', 'completed_at')
    search_fields = ('module__title', 'user__email')
    ordering = ('-completed_at',)

@admin.register(CourseAssessment)
class CourseAssessmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'total_score', 'max_score', 'time_spent', 'completed_at')
    list_filter = ('course', 'completed_at')
    search_fields = ('course__name', 'user__email')
    ordering = ('-completed_at',)
    filter_horizontal = ('module_assessments',)