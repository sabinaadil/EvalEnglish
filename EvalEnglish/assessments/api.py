from uuid import UUID
from courses.api import IsTeacher
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from courses.models import Module
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