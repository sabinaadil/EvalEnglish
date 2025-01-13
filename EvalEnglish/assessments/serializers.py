from rest_framework import serializers
from .models import QuestionType, Question, AnswerOption, UserAnswer, ModuleAssessment, CourseAssessment

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ('id', 'name', 'description')

class QuestionSerializer(serializers.ModelSerializer):
    question_type = QuestionTypeSerializer()

    class Meta:
        model = Question
        fields = ('id', 'module', 'question_text', 'question_type', 'question_file_url', 'time_limit', 'max_attempts', 'max_score', 'correct_answer', 'created_at')
        read_only_fields = ('id', 'created_at')

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'question', 'answer_text', 'is_correct')
        read_only_fields = ('id',)

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = (
            'id', 'question', 'user', 'answer_text', 'answer_file_url',
            'attempt_number', 'time_spent', 'is_correct', 'teacher_score',
            'model_score', 'final_score', 'score', 'submitted_at', 'is_late'
        )
        read_only_fields = ('id', 'submitted_at', 'is_correct', 'final_score', 'score')

class ModuleAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleAssessment
        fields = ('id', 'module', 'score', 'max_score', 'completed_at')

class CourseAssessmentSerializer(serializers.ModelSerializer):
    module_assessments = ModuleAssessmentSerializer(many=True)

    class Meta:
        model = CourseAssessment
        fields = ('id', 'course', 'user', 'total_score', 'max_score', 'time_spent', 'completed_at', 'module_assessments')
        read_only_fields = ('id', 'completed_at', 'total_score', 'max_score', 'time_spent')