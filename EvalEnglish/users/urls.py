from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api, teacher_applications_api

urlpatterns = [
    path('signup/', api.sign_up, name='sign_up'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('me/', api.me, name='me'),
    path('editprofile/', api.edit_profile, name='editprofile'),
    path('editpassword/', api.edit_password, name='editpassword'),

    path('teacher-application/', api.teacher_application_view, name='teacher_application_view'),
    path('teacher-applications/pending_count/', teacher_applications_api.pending_teacher_applications_count, name='pending_apps_count'),
    path('teacher-applications/pending_list/', teacher_applications_api.pending_teacher_applications_list, name='pending_apps_list'),
    path('teacher-applications/<uuid:application_id>/', teacher_applications_api.teacher_application_detail, name='teacher_app_detail'),
    path('teacher-applications/<uuid:application_id>/approve/', teacher_applications_api.teacher_application_approve, name='teacher_app_approve'),
    path('teacher-applications/<uuid:application_id>/reject/', teacher_applications_api.teacher_application_reject, name='teacher_app_reject'),
]
