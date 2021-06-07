from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=40, required=True, widget=forms.EmailInput, label="Email")
    login = forms.CharField(max_length=40, label="Логин пользователя", required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    address = forms.CharField(label="Адрес", max_length=40, required=False)
    first_name = forms.CharField(max_length=40, label="Имя", required=False)
    last_name = forms.CharField(max_length=40, label="Фамиля", required=False)
    phone_number = forms.CharField(max_length=17, label="Номер телефона", required=False)

    class Meta:
        model = User
        fields = ('email', 'login', 'password1', 'password2', 'first_name', 'last_name', 'address', 'phone_number')


class SignInForm(forms.Form):

    email = forms.EmailField(max_length=40, required=True, widget=forms.EmailInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Пароль")

    class Meta:
        model = User
        fields = ('email', 'password')


# class ChangeUserForm(UserChangeForm):
#
#     class Meta:
#         model = User
#         fields = ('email', 'login', 'password', 'birth_date', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_admin')
