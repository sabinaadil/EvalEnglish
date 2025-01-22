from django.urls import path
from . import api

urlpatterns = [
    path('notifications/', api.notifications_list, name='notifications_list'),
    path('notifications/<uuid:notif_id>/read/', api.mark_notification_read, name='mark_notification_read'),
    path('<uuid:notif_id>/read/', api.mark_notification_read, name='mark_notification_read'),
    path('notifications/unread_count/', api.unread_notifications_count, name='unread_notifications_count'),
]