from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create(self, email, password, username, **fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, username, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', False)
        return self._create(email, password, username, **fields)

    def create_superuser(self, email, password, username, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', True)
        return self._create(email, password, username, **fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=5, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(5)
        self.activation_code = code
        self.save()
        return code

    def get_all_permissions(self, obj=None):
        return ''

