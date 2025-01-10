from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.sign_up, name='sign_up'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('editprofile/', api.edit_profile, name='editprofile'),
    path('editpassword/', api.edit_password, name='editpassword'),
   
]