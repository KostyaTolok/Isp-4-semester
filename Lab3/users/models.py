from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):

    email = models.EmailField(verbose_name="Email", max_length=40, unique=True)
    login = models.CharField(verbose_name="Имя пользователя", max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    first_name = models.CharField(verbose_name="Имя пользователя", max_length=40, blank=True)
    last_name = models.CharField(verbose_name="Фамилия пользователя", max_length=40, blank=True)
    phone_number = models.CharField(max_length=17, blank=True)

    def __str__(self):
        return self.user.email
