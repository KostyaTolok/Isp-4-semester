from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, UserProfile


class SignUpForm(UserCreationForm):

    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'login', 'password1', 'password2', 'birth_date', 'first_name', 'last_name', 'phone_number')


class SignInForm(AuthenticationForm):
    pass


class ChangeUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'login', 'password', 'birth_date', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_admin')
