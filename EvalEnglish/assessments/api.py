from uuid import UUID
from users.models import User
from courses.api import IsTeacher
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from courses.models import Module, Course
from django.db.models import Q
from django.utils import timezone
from .utils import update_user_answer_after_review
from .models import QuestionType, Question, AnswerOption, UserAnswer, ModuleAssessment, CourseAssessment
from .serializers import (QuestionTypeSerializer, QuestionSerializer, AnswerOptionSerializer, UserAnswerCreateSerializer,
                          ModuleAssessmentSerializer, CourseAssessmentSerializer, UserAnswerSerializer)

class QuestionTypeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        types = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(types, many=True)
        return Response(serializer.data)


class QuestionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=201)
        return Response(serializer.errors, status=400)


class ModuleQuestionsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, module_id):
        try:
            UUID(str(module_id))  # validate UUID
            module = Module.objects.get(id=module_id)
        except (Module.DoesNotExist, ValueError):
            return Response({'error': 'Модуль не найден'}, status=404)

        questions = module.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionSingleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return None

    def get(self, request, question_id):
        question = self.get_object(question_id)
        if not question:
            return Response({'error': 'Вопрос не найден'}, status=404)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, question_id):
        question = self.get_object(question_id)
        if not question:
            return Response({'error': 'Вопрос не найден'}, status=404)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Вопрос обновлён', 'question': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, question_id):
        question = self.get_object(question_id)
        if not question:
            return Response({'error': 'Вопрос не найден'}, status=404)
        question.delete()
        return Response({'message': 'Вопрос удалён'})


class AnswerOptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnswerOptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Вариант ответа создан', 'option': serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class QuestionAnswerOptionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, question_id):
        options = AnswerOption.objects.filter(question_id=question_id)
        serializer = AnswerOptionSerializer(options, many=True)
        return Response(serializer.data)


class AnswerOptionSingleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, option_id):
        try:
            return AnswerOption.objects.get(id=option_id)
        except AnswerOption.DoesNotExist:
            return None

    def get(self, request, option_id):
        option = self.get_object(option_id)
        if not option:
            return Response({'error': 'Вариант ответа не найден'}, status=404)
        serializer = AnswerOptionSerializer(option)
        return Response(serializer.data)

    def put(self, request, option_id):
        option = self.get_object(option_id)
        if not option:
            return Response({'error': 'Вариант ответа не найден'}, status=404)
        serializer = AnswerOptionSerializer(option, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Вариант ответа обновлён', 'option': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, option_id):
        option = self.get_object(option_id)
        if not option:
            return Response({'error': 'Вариант ответа не найден'}, status=404)
        option.delete()
        return Response({'message': 'Вариант ответа удалён'})


class UserAnswerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserAnswerCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            answer = serializer.save()
            response_serializer = UserAnswerSerializer(answer)
            return Response({
                'message': 'Ответ сохранён',
                'answer': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUserAnswersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Вопрос не найден'}, status=404)

        answers = UserAnswer.objects.filter(question=question, user=request.user)
        serializer = UserAnswerCreateSerializer(answers, many=True)
        return Response(serializer.data)


class UserAnswerSingleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, answer_id, user):
        try:
            answer = UserAnswer.objects.get(id=answer_id)
        except UserAnswer.DoesNotExist:
            return Response({'error': 'Ответ не найден'}, status=404)

        if answer.user != user:
            return Response({'error': 'Вы не являетесь автором этого ответа'}, status=403)

        return answer

    def get(self, request, answer_id):
        answer = self.get_object(answer_id, request.user)
        if isinstance(answer, Response):
            return answer
        serializer = UserAnswerCreateSerializer(answer)
        return Response(serializer.data)


class GradeUserAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, answer_id):
        try:
            answer = UserAnswer.objects.get(id=answer_id)
        except UserAnswer.DoesNotExist:
            return Response({'error': 'Ответ не найден'}, status=404)

        teacher_score = request.data.get('teacher_score')
        if teacher_score is None:
            return Response({'error': 'Оценка преподавателя обязательна'}, status=400)

        try:
            answer.teacher_score = float(teacher_score)
        except ValueError:
            return Response({'error': 'Неверный формат оценки'}, status=400)

        update_user_answer_after_review(answer)

        serializer = UserAnswerSerializer(answer)
        return Response({'message': 'Оценка сохранена', 'answer': serializer.data}, status=200)


class ModuleAssessmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, module_id):
        user = request.user

        # Проверка существования модуля
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({'error': 'Модуль не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Подсчёт всех баллов за ответы пользователя в этом модуле
        user_answers = UserAnswer.objects.filter(user=user, question__module=module)
        total_score = sum(answer.score for answer in user_answers)

        # Подсчёт максимального возможного балла по всем вопросам модуля
        questions = Question.objects.filter(module=module)
        max_score = sum(question.max_score for question in questions)

        # Получение или создание оценки
        assessment, created = ModuleAssessment.objects.get_or_create(
            module=module,
            user=user,
            defaults={
                'score': total_score,
                'max_score': max_score,
            }
        )

        # Обновляем данные, если они изменились (на случай, если пользователь прошёл часть позже)
        if not created:
            assessment.score = total_score
            assessment.max_score = max_score
            assessment.save()

        serializer = ModuleAssessmentSerializer(assessment)
        return Response(serializer.data)


class ModuleAssessmentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ModuleAssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModuleAssessmentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assessments = ModuleAssessment.objects.filter(user=request.user)
        serializer = ModuleAssessmentSerializer(assessments, many=True)
        return Response(serializer.data)


class ModuleAssessmentSingleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_id):
        try:
            assessment = ModuleAssessment.objects.get(id=assessment_id, user=request.user)
        except ModuleAssessment.DoesNotExist:
            return Response({'error': 'Оценка не найдена'}, status=404)

        serializer = ModuleAssessmentSerializer(assessment)
        return Response(serializer.data)

class CourseAssessmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        user = request.user

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        assessment, _ = CourseAssessment.objects.get_or_create(course=course, user=user)

        modules = Module.objects.filter(course=course)
        module_assessments = []

        total_score = 0
        max_total_score = 0
        total_time_spent = 0

        for module in modules:
            # Получаем все вопросы модуля
            questions = module.questions.all()
            # Получаем все ответы пользователя на эти вопросы
            user_answers = UserAnswer.objects.filter(user=user, question__in=questions)

            # Подсчитываем сумму баллов и максимальную оценку
            module_score = sum([ua.score for ua in user_answers])
            module_max_score = sum([q.max_score for q in questions])
            module_time_spent = sum([ua.time_spent for ua in user_answers])

            total_score += module_score
            max_total_score += module_max_score
            total_time_spent += module_time_spent

            # Получаем или создаём оценку за модуль
            module_assessment, _ = ModuleAssessment.objects.get_or_create(
                module=module,
                user=user,
                defaults={
                    'score': module_score,
                    'max_score': module_max_score
                }
            )

            # Обновляем данные, если они изменились
            if module_assessment.score != module_score or module_assessment.max_score != module_max_score:
                module_assessment.score = module_score
                module_assessment.max_score = module_max_score
                module_assessment.save()

            module_assessments.append(module_assessment)

        # Обновляем CourseAssessment
        assessment.total_score = total_score
        assessment.max_score = max_total_score
        assessment.time_spent = total_time_spent
        assessment.save()
        assessment.module_assessments.set(module_assessments)

        serializer = CourseAssessmentSerializer(assessment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class StudentAnswersReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, student_id):
        course_id = request.query_params.get("course")
        if not course_id:
            return Response({"error": "Параметр 'course' обязателен."}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден."}, status=404)

        questions = Question.objects.filter(
            module__course=course
        ).filter(
            Q(question_type__name__iexact="text") | Q(question_type__name__iexact="file")
        ).distinct()

        question_serializer = QuestionSerializer(questions, many=True)

        last_answers = []
        for q in questions:
            last_answer = (
                UserAnswer.objects.filter(user__id=student_id, question=q)
                .order_by('-submitted_at')
                .first()
            )
            if last_answer:
                last_answers.append(last_answer)

        answer_serializer = UserAnswerSerializer(last_answers, many=True)

        return Response({
            "questions": question_serializer.data,
            "answers": answer_serializer.data
        }, status=status.HTTP_200_OK)