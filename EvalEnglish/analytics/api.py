from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Avg, Sum
from .models import ActivityMetrics
from .serializers import ActivityMetricsSerializer
from courses.models import Course
from assessments.models import UserAnswer
from ml.model_utils import evaluate_final_efficiency_score

class ActivityMetricsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        course_id = request.query_params.get('course_id')

        if course_id:
            user_answers = UserAnswer.objects.filter(user=user, question__module__course__id=course_id)
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({'error': 'Курс не найден'}, status=404)
        else:
            user_answers = UserAnswer.objects.filter(user=user)
            course = None

        tasks_completed = user_answers.count()
        avg_score = user_answers.aggregate(avg=Avg('score'))['avg'] or 0
        avg_teacher_score = user_answers.aggregate(avg=Avg('teacher_score'))['avg'] or 0
        avg_model_score = user_answers.aggregate(avg=Avg('model_score'))['avg'] or 0
        total_time = user_answers.aggregate(total=Sum('time_spent'))['total'] or 0
        avg_attempts = user_answers.aggregate(avg=Avg('attempt_number'))['avg'] or 0
        late_count = user_answers.filter(is_late=True).count()

        metrics_data = {
            'tasks_completed': tasks_completed,
            'average_score': avg_score,
            'average_teacher_score': avg_teacher_score,
            'average_model_score': avg_model_score,
            'time_spent': total_time,
            'avg_attempts': avg_attempts,
            'late_submissions': late_count
        }

        efficiency = evaluate_final_efficiency_score(metrics_data)

        metrics, _ = ActivityMetrics.objects.update_or_create(
            user=user,
            course=course,
            activity_date=timezone.now().date(),
            defaults={
                'tasks_completed': tasks_completed,
                'average_score': round(avg_score, 2),
                'average_teacher_score': round(avg_teacher_score, 2),
                'average_model_score': round(avg_model_score, 2),
                'time_spent': total_time,
                'avg_attempts': round(avg_attempts, 2),
                'late_submissions': late_count,
                'final_efficiency_score': efficiency,
            }
        )

        serializer = ActivityMetricsSerializer(metrics)
        return Response(serializer.data)
