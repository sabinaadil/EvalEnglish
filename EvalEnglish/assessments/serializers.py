from rest_framework import serializers
from django.utils import timezone
from common.serializers import DocumentSerializer
from notifications.models import Notification
from .utils import evaluate_text_answer, extract_text_from_file
from .models import QuestionType, Question, AnswerOption, UserAnswer, ModuleAssessment, CourseAssessment

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ('id', 'name', 'description')

class QuestionSerializer(serializers.ModelSerializer):
    question_file_url = DocumentSerializer(many=True, read_only=True)

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
    answer_file_url = DocumentSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserAnswer
        fields = (
            'id', 'question', 'user', 'user_email',
            'answer_text', 'answer_file_url',
            'attempt_number', 'time_spent',
            'is_correct', 'teacher_score', 'model_score', 'final_score', 'score',
            'submitted_at', 'is_late'
        )
        read_only_fields = fields



class UserAnswerCreateSerializer(serializers.ModelSerializer):
    answer_file_url = DocumentSerializer(many=True, required=False)

    class Meta:
        model = UserAnswer
        fields = ('id', 'question', 'answer_text', 'answer_file_url', 'time_spent')

    def validate(self, attrs):
        user = self.context['request'].user
        question = attrs['question']

        previous_attempts = UserAnswer.objects.filter(user=user, question=question).count()
        if previous_attempts >= question.max_attempts:
            raise serializers.ValidationError("Превышено максимальное количество попыток для этого вопроса.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        answer_text = validated_data.get('answer_text', '')
        answer_files = validated_data.pop('answer_file_url', [])

        previous_attempts = UserAnswer.objects.filter(user=user, question=question).count()
        attempt_number = previous_attempts + 1

        is_late = False
        if question.time_limit and validated_data['time_spent'] > question.time_limit:
            is_late = True

        question_type = question.question_type.name.lower()

        is_correct = False
        model_score = None
        teacher_score = None
        final_score = None
        score = 0

        if question_type in ['boolean', 'quiz']:
            is_correct = (answer_text.strip().lower() == question.correct_answer.strip().lower())
            score = question.max_score if is_correct else 0
            final_score = score

        elif question_type == 'text':
            if answer_text.strip():
                model_score = evaluate_text_answer(answer_text, question.correct_answer)
            else:
                Notification.objects.create(
                    user=question.module.course.teacher,
                    notification_type='info',
                    message=f"Студент отправил текстовый ответ на вопрос: {question.question_text[:50]}"
                )

        elif question_type == 'file' and answer_files:
            file_instance = answer_files[0]
            file_path = file_instance.file.path
            extracted_text = extract_text_from_file(file_path)

            if extracted_text:
                model_score = evaluate_text_answer(extracted_text, question.correct_answer)
            else:
                Notification.objects.create(
                    user=question.module.course.teacher,
                    notification_type='info',
                    message=f"Файл ответа от студента требует проверки вручную: {question.question_text[:50]}"
                )

        user_answer = UserAnswer.objects.create(
            user=user,
            question=question,
            answer_text=validated_data.get('answer_text'),
            time_spent=validated_data.get('time_spent', 0),
            attempt_number=attempt_number,
            is_correct=is_correct,
            teacher_score=teacher_score,
            model_score=model_score,
            final_score=final_score,
            score=score,
            is_late=is_late
        )

        if 'answer_file_url' in validated_data:
            user_answer.answer_file_url.set(validated_data['answer_file_url'])

        return user_answer


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