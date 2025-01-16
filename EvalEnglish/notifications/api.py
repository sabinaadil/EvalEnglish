from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from users.models import TeacherApplication

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications_list(request):
    """Список уведомлений для текущего пользователя."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notif_id):
    """Пометить одно уведомление как прочитанное."""
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return Response({'detail': 'Notification marked as read'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_application_approve(request, application_id):
    """
    Пример подтверждения заявки. Только для админов (is_superuser).
    """
    if not request.user.is_superuser:
        return Response({'detail': 'У вас нет прав одобрять заявки.'}, status=403)
    
    application = get_object_or_404(TeacherApplication, id=application_id)
    application.status = 'approved'
    application.reviewed_at = application.reviewed_at or application.submitted_at
    application.save()

    user = application.user
    user.is_teacher = True
    user.save()

    return Response({'detail': 'Заявка одобрена.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_application_reject(request, application_id):
    """
    Пример отклонения заявки. Только для админов (is_superuser).
    """
    if not request.user.is_superuser:
        return Response({'detail': 'У вас нет прав отклонять заявки.'}, status=403)
    
    application = get_object_or_404(TeacherApplication, id=application_id)
    application.status = 'rejected'
    application.reviewed_at = application.reviewed_at or application.submitted_at
    application.save()

    return Response({'detail': 'Заявка отклонена.'})
