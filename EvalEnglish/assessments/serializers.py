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


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'question', 'answer_text', 'is_correct')
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    question_file_url = DocumentSerializer(many=True, read_only=True)
    # Добавляем вложенное поле для вариантов ответа; required=False чтобы не было ошибки, если не передают
    answer_options = AnswerOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = (
            'id', 'module', 'question_text', 'question_type', 'question_file_url',
            'time_limit', 'max_attempts', 'max_score', 'correct_answer', 'created_at',
            'answer_options'
        )
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        answer_options_data = validated_data.pop('answer_options', [])
        question = Question.objects.create(**validated_data)
        for option_data in answer_options_data:
            AnswerOption.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        answer_options_data = validated_data.pop('answer_options', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if answer_options_data is not None:
            # Один из вариантов — удаляем старые и создаем новые варианты.
            instance.answer_options.all().delete()
            for option_data in answer_options_data:
                AnswerOption.objects.create(question=instance, **option_data)
        return instance


class UserAnswerSerializer(serializers.ModelSerializer):
    answer_file_url = DocumentSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)

    class Meta:
        model = UserAnswer
        fields = (
            'id', 'question', 'user', 'user_email',
            'answer_text', 'answer_file_url',
            'attempt_number', 'time_spent',
            'is_correct', 'teacher_score', 'model_score', 'final_score', 'score',
            'submitted_at', 'is_late', 'question_type',
        )
        read_only_fields = fields


class UserAnswerCreateSerializer(serializers.ModelSerializer):
    answer_file_url = DocumentSerializer(many=True, required=False)

    class Meta:
        model = UserAnswer
        fields = ('id', 'question', 'answer_text', 'answer_file_url', 'time_spent', 'is_correct', 'model_score',)

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
            correct_options = AnswerOption.objects.filter(question=question, is_correct=True).values_list('answer_text',
                                                                                                          flat=True)
            is_correct = answer_text.strip().lower() in [opt.strip().lower() for opt in correct_options]

            score = question.max_score if is_correct else 0
            final_score = score
            teacher_score = None
            model_score = None

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
    score = serializers.SerializerMethodField()

    class Meta:
        model = ModuleAssessment
        fields = ('id', 'module', 'user', 'score', 'max_score', 'completed_at')

    def get_score(self, obj):
        user_answers = obj.module.questions.all().first().user_answers.all()  # упрощенный пример; измените по необходимости
        total_score = sum([ans.final_score or ans.score for ans in user_answers])

        if total_score >= obj.max_score * 0.9 and not obj.completed_at:
            obj.completed_at = timezone.now()
            obj.score = total_score
            obj.save()

        return int(total_score)


class CourseAssessmentSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    max_score = serializers.SerializerMethodField()
    time_spent = serializers.SerializerMethodField()

    class Meta:
        model = CourseAssessment
        fields = (
            'id', 'course', 'user',
            'total_score', 'max_score', 'time_spent',
            'completed_at', 'module_assessments'
        )

    def get_total_score(self, obj):
        return sum([a.score for a in obj.module_assessments.all()])

    def get_max_score(self, obj):
        return sum([a.max_score for a in obj.module_assessments.all()])

    def get_time_spent(self, obj):
        return sum([
            sum([ua.time_spent for ua in UserAnswer.objects.filter(
                user=obj.user,
                question__module=module_assessment.module
            )])
            for module_assessment in obj.module_assessments.all()
        ])
