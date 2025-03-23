from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Course, Module, Lesson, CourseParticipant
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer, CourseParticipantSerializer
from rest_framework.pagination import PageNumberPagination


class IsTeacher:
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response({'message': 'Курс создан', 'course': serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class CoursesListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        courses = Course.objects.filter(teacher=request.user)

        paginator = PageNumberPagination()
        paginated_courses = paginator.paginate_queryset(courses, request)
        serializer = CourseSerializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)


class CourseSingleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_course_or_error(self, course_id, user):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=404)

        if course.teacher != user:
            return Response({'error': 'Вы не являетесь автором курса'}, status=403)

        return course

    def get(self, request, course_id):
        course = self.get_course_or_error(course_id, request.user)
        if isinstance(course, Response):
            return course
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, course_id):
        course = self.get_course_or_error(course_id, request.user)
        if isinstance(course, Response):
            return course
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Курс обновлён', 'course': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, course_id):
        course = self.get_course_or_error(course_id, request.user)
        if isinstance(course, Response):
            return course
        course.delete()
        return Response({'message': 'Курс удалён'})


class ModuleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.validated_data['course']
            if course.teacher != request.user:
                return Response({'error': 'Вы не являетесь автором курса'}, status=403)
            serializer.save()
            return Response({'message': 'Модуль создан', 'module': serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class ModulesListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=404)

        if course.teacher != request.user:
            return Response({'error': 'Вы не являетесь автором курса'}, status=403)

        modules = Module.objects.filter(course=course).order_by('order')
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)


class ModuleSingleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_module_or_error(self, module_id, user):
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({'error': 'Модуль не найден'}, status=404)

        if module.course.teacher != user:
            return Response({'error': 'Вы не являетесь автором курса'}, status=403)

        return module

    def get(self, request, module_id):
        module = self.get_module_or_error(module_id, request.user)
        if isinstance(module, Response):
            return module
        serializer = ModuleSerializer(module)
        return Response(serializer.data)

    def put(self, request, module_id):
        module = self.get_module_or_error(module_id, request.user)
        if isinstance(module, Response):
            return module
        serializer = ModuleSerializer(module, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Модуль обновлён', 'module': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, module_id):
        module = self.get_module_or_error(module_id, request.user)
        if isinstance(module, Response):
            return module
        module.delete()
        return Response({'message': 'Модуль удалён'})


class LessonAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            module = serializer.validated_data['module']
            if module.course.teacher != request.user:
                return Response({'error': 'Вы не являетесь автором курса'}, status=403)
            serializer.save()
            return Response({'message': 'Урок создан', 'lesson': serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class LessonsListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request, module_id):
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({'error': 'Модуль не найден'}, status=404)

        if module.course.teacher != request.user:
            return Response({'error': 'Вы не являетесь автором курса'}, status=403)

        lessons = Lesson.objects.filter(module=module).order_by('order')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonSingleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_lesson_or_error(self, lesson_id, user):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'Урок не найден'}, status=404)

        if lesson.module.course.teacher != user:
            return Response({'error': 'Вы не являетесь автором курса'}, status=403)

        return lesson

    def get(self, request, lesson_id):
        lesson = self.get_lesson_or_error(lesson_id, request.user)
        if isinstance(lesson, Response):
            return lesson
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, lesson_id):
        lesson = self.get_lesson_or_error(lesson_id, request.user)
        if isinstance(lesson, Response):
            return lesson
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Урок обновлён', 'lesson': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, lesson_id):
        lesson = self.get_lesson_or_error(lesson_id, request.user)
        if isinstance(lesson, Response):
            return lesson
        lesson.delete()
        return Response({'message': 'Урок удалён'})


class EnrollCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=404)

        if CourseParticipant.objects.filter(course=course, participant=request.user).exists():
            return Response({'error': 'Вы уже зарегистрированы на этот курс'}, status=400)

        participant = CourseParticipant.objects.create(course=course, participant=request.user)
        serializer = CourseParticipantSerializer(participant)
        return Response({'message': 'Успешная регистрация на курс', 'participant': serializer.data})


class CourseParticipantsListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=404)

        if course.teacher != request.user:
            return Response({'error': 'Вы не являетесь автором курса'}, status=403)

        participants = CourseParticipant.objects.filter(course=course)
        serializer = CourseParticipantSerializer(participants, many=True)
        return Response(serializer.data)


class LeaveCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=404)

        try:
            participant = CourseParticipant.objects.get(course=course, participant=request.user)
        except CourseParticipant.DoesNotExist:
            return Response({'error': 'Вы не зарегистрированы на этот курс'}, status=400)

        participant.delete()
        return Response({'message': 'Вы успешно отписались от курса'})


class MyCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        participations = CourseParticipant.objects.filter(participant=request.user)
        courses = [p.course for p in participations]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)