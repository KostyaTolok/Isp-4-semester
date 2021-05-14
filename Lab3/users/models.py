from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, login, email, password):
        if not email:
            raise ValueError('Email must be specified')

        user = self.model(email=email, login=login)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, login, password=None):
        user = self.create_user(email=email, login=login, password=password)

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):

    email = models.EmailField(verbose_name="Email", max_length=40, unique=True)
    login = models.CharField(verbose_name="Логин пользователя", max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class UserProfile(models.Model):

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    first_name = models.CharField(verbose_name="Имя пользователя", max_length=40, blank=True)
    last_name = models.CharField(verbose_name="Фамилия пользователя", max_length=40, blank=True)
    phone_number = models.CharField(max_length=17, blank=True)

    def __str__(self):
        return self.user.email

