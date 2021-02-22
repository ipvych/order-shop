from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    phone = models.CharField(_('phone number'), unique=True, max_length=64)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['email']
        verbose_name = _('user')
        verbose_name_plural = _('users')
