from rest_framework import serializers
from .models import Notification
from users.models import TeacherApplication

class NotificationSerializer(serializers.ModelSerializer):
    action_url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'message', 'is_read', 'created_at', 'action_url']

    def get_action_url(self, obj):
        """Возвращает URL для действий, связанных с уведомлением."""
        if obj.notification_type == "info":
            return None  # Информационные уведомления не требуют перехода
        elif obj.notification_type == "reminder":
            return "/admin/notifications/"  # Пример ссылки для админа
        elif obj.notification_type == "warning":
            application = TeacherApplication.objects.filter(user=obj.user).first()
            if application:
                return f"/teacher-application/"  # Пример ссылки на заявку
        return None  # Для типов уведомлений без действия
