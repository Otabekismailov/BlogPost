from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)

from users.manger import CustomUserManager


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
