from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import SignUpForm, ProfileForm



@api_view(['GET'])
def me(request):
    user = request.user
    
    return JsonResponse({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'avatar': user.get_avatar(),
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def sign_up(request):
    data = request.data
    message = 'success'

    form = SignUpForm(data)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        form.save()

        user_id = str(user.id).replace('-', '')

        url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user_id}'

        send_mail(
            "Пожалуйста, подтвердите свою почту",
            f"Для подтверждения почты перейдите по ссылке: {url}",
            "noreply@wey.com",
            [user.email],
            fail_silently=False,
        )
    else:
        message = form.errors

    return JsonResponse({'message': message}, safe=False)

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')
    
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Почта уже существует!'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)
 
        return JsonResponse({'message': 'success info updated', 'user': serializer.data})

@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'success password updated'})
    else:
        return JsonResponse({'message': form.errors}, safe=False)
