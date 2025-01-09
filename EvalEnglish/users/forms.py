from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'avatar']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'avatar']