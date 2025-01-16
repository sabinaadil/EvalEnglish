from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    is_teacher_applicant = forms.BooleanField(
        required=False,
        label="Я преподаватель",
        help_text="Отметьте, если хотите подать заявку на преподавателя."
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'avatar',
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']