from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import User, TeacherApplication
from .forms import SignUpForm, ProfileForm
from .serializers import UserSerializer, TeacherApplicationSerializer
from common.models import Document
from common.serializers import DocumentSerializer

# Импортируем Notification
from notifications.models import Notification

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def sign_up(request):
    data = request.data
    form = SignUpForm(data)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False  # wait for email confirmation

        # Check if user is applying to be a teacher
        is_teacher_applicant = form.cleaned_data.get('is_teacher_applicant', False)
        if is_teacher_applicant:
            user.role = 'teacher'
            user.is_teacher = False
        else:
            user.role = 'student'
            user.is_teacher = False

        user.save()

        # Send verification email
        user_id = str(user.id).replace('-', '')
        activation_url = f"{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user_id}"
        send_mail(
            "Подтвердите вашу почту",
            f"Перейдите по ссылке для активации аккаунта: {activation_url}",
            "noreply@evalenglish.com",
            [user.email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'success'}, status=201)
    else:
        return JsonResponse({'message': form.errors}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user
    data = request.data
    if 'email' in data:
        email = data.get('email')
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            return Response({'message': 'Почта уже существует!'}, status=400)
    form = ProfileForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        serializer = UserSerializer(user, context={'request': request})
        return Response({'message': 'success info updated', 'user': serializer.data}, status=200)
    else:
        return Response({'message': form.errors}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()
        return Response({'message': 'success password updated'}, status=200)
    else:
        return Response({'message': form.errors}, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_application_view(request):
    user = request.user

    if user.role != 'teacher':
        return Response({'detail': 'Вы не отмечены как преподаватель.'}, status=400)

    if request.method == 'GET':
        try:
            application = user.teacher_application
            serializer = TeacherApplicationSerializer(application, context={'request': request})
            return Response(serializer.data)
        except TeacherApplication.DoesNotExist:
            return Response({'detail': 'Заявка не найдена.'}, status=404)

    if request.method == 'POST':
        full_name = request.data.get('full_name')
        phone = request.data.get('phone')
        file = request.FILES.get('document')

        application, created = TeacherApplication.objects.get_or_create(user=user)
        application.full_name = full_name or application.full_name
        application.phone = phone or application.phone
        application.status = 'pending'
        application.submitted_at = timezone.now()
        application.reviewed_at = None  
        application.rejection_reason = None  
        application.save()

        # Если новая заявка => создаём уведомления для всех админов
        if created:
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='info',
                    message=f"Новая заявка на преподавателя: {application.full_name} ({user.email})"
                )

        if file:
            # Удаляем существующие документы перед добавлением нового
            existing_documents = Document.objects.filter(
                content_type=ContentType.objects.get_for_model(TeacherApplication),
                object_id=application.id
            )
            existing_documents.delete()

            # Создаём новый Document, связанный с TeacherApplication
            teacher_app_ct = ContentType.objects.get_for_model(TeacherApplication)
            document = Document.objects.create(
                uploaded_by=user,
                content_type=teacher_app_ct,
                object_id=application.id,
                file=file
            )

        serializer = TeacherApplicationSerializer(application, context={'request': request})
        return Response(serializer.data, status=201)
