from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Avg, Sum
from rest_framework import status
from .models import ActivityMetrics
from .serializers import ActivityMetricsSerializer
from courses.models import Course
from assessments.models import UserAnswer
from ml.model_utils import evaluate_final_efficiency_score
from users.models import User

class ActivityMetricsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_id = request.query_params.get('student_id')
        course_id = request.query_params.get('course_id')
        today = timezone.now().date()

        # Определяем, какие курсы учитывать
        if request.user.is_teacher:
            courses_qs = Course.objects.filter(teacher=request.user)
        else:
            courses_qs = Course.objects.filter(participants__participant=request.user)

        if course_id:
            try:
                course = courses_qs.get(id=course_id)
                courses_ids = [course_id]
            except Course.DoesNotExist:
                return Response({'error': 'Курс не найден'}, status=404)
        else:
            course = None
            courses_ids = courses_qs.values_list('id', flat=True)

        if student_id:
            try:
                user = User.objects.get(id=student_id)
            except User.DoesNotExist:
                return Response({'error': 'Студент не найден.'}, status=404)
            user_answers = UserAnswer.objects.filter(
                user=user,
                question__module__course__id__in=courses_ids
            )
        else:
            user_answers = UserAnswer.objects.filter(
                question__module__course__id__in=courses_ids
            )

        # Вычисляем агрегированные показатели
        tasks_completed = user_answers.count()
        avg_score = user_answers.aggregate(avg=Avg('score'))['avg'] or 0
        avg_teacher_score = user_answers.aggregate(avg=Avg('teacher_score'))['avg'] or 0
        avg_model_score = user_answers.aggregate(avg=Avg('model_score'))['avg'] or 0
        total_time = user_answers.aggregate(total=Sum('time_spent'))['total'] or 0
        avg_attempts = user_answers.aggregate(avg=Avg('attempt_number'))['avg'] or 0
        late_count = user_answers.filter(is_late=True).count()

        metrics_data = {
            'tasks_completed': tasks_completed,
            'average_score': round(avg_score, 2),
            'average_teacher_score': round(avg_teacher_score, 2),
            'average_model_score': round(avg_model_score, 2),
            'time_spent': total_time,
            'avg_attempts': round(avg_attempts, 2),
            'late_submissions': late_count,
        }

        efficiency = evaluate_final_efficiency_score(metrics_data)
        metrics_data['final_efficiency_score'] = efficiency

        if course_id and student_id:
            metrics, _ = ActivityMetrics.objects.update_or_create(
                user=user,
                course=course,
                activity_date=today,
                defaults=metrics_data
            )
            serializer = ActivityMetricsSerializer(metrics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(metrics_data, status=status.HTTP_200_OK)
