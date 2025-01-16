from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TeacherApplication, User
from notifications.models import Notification
from .serializers import TeacherApplicationSerializer
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_teacher_applications_count(request):
    """Вернуть количество заявок в статусе pending."""
    if not request.user.is_superuser:
        return Response({'count': 0})
    count = TeacherApplication.objects.filter(status='pending').count()
    return Response({'count': count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_teacher_applications_list(request):
    """Вернуть список заявок (статус pending), только если пользователь админ."""
    if not request.user.is_superuser:
        return Response({'detail': 'Недостаточно прав'}, status=403)
    apps = TeacherApplication.objects.filter(status='pending').order_by('-submitted_at')
    serializer = TeacherApplicationSerializer(apps, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_application_detail(request, application_id):
    """Детальный просмотр одной заявки."""
    if not request.user.is_superuser:
        return Response({'detail': 'Недостаточно прав'}, status=403)
    application = get_object_or_404(TeacherApplication, id=application_id)
    serializer = TeacherApplicationSerializer(application)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_application_approve(request, application_id):
    """Админ: одобрить заявку."""
    if not request.user.is_superuser:
        return Response({'detail': 'Недостаточно прав'}, status=403)

    application = get_object_or_404(TeacherApplication, id=application_id)
    application.status = 'approved'
    application.reviewed_at = timezone.now()
    application.save()

    user = application.user
    user.is_teacher = True
    user.save()

    return Response({'detail': 'Заявка одобрена'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def teacher_application_reject(request, application_id):
    """Админ: отклонить заявку с причиной."""
    application = get_object_or_404(TeacherApplication, id=application_id)
    reason = request.data.get('reason', '').strip()

    if not reason:
        return Response({'detail': 'Пожалуйста, укажите причину отклонения.'}, status=400)

    application.status = 'rejected'
    application.reviewed_at = timezone.now()
    application.rejection_reason = reason  
    application.save()

    Notification.objects.create(
        user=application.user,
        notification_type='info',
        message=f"Ваша заявка на преподавателя была отклонена. Причина: {reason}"
    )

    return Response({'detail': 'Заявка отклонена'}, status=200)
