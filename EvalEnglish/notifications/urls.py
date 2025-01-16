from django.urls import path
from . import api

urlpatterns = [
    path('', api.notifications_list, name='notifications_list'),
    path('<uuid:notif_id>/read/', api.mark_notification_read, name='mark_notification_read'),

    path('approve/<uuid:application_id>/', api.teacher_application_approve, name='teacher_application_approve'),
    path('reject/<uuid:application_id>/', api.teacher_application_reject, name='teacher_application_reject'),
]
