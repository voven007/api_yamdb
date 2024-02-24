from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from users.constants import MAX_LEN_EMAIL, MAX_LEN_ROLE, MAX_LEN_USERNAME

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = ((USER, 'Аутентифицированный пользователь'),
         (MODERATOR, 'Модератор'),
         (ADMIN, 'Администратор'))


class MyUser(AbstractUser):
    """Модель прользователей"""
    username = models.CharField(
        max_length=MAX_LEN_USERNAME,
        unique=True,
        null=False,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ в имени пользователя'
        )])
    email = models.EmailField(
        max_length=MAX_LEN_EMAIL,
        unique=True,
        blank=False,
        null=False)
    first_name = models.CharField(
        max_length=MAX_LEN_USERNAME,
        blank=True)
    last_name = models.CharField(
        max_length=MAX_LEN_USERNAME,
        blank=True)
    bio = models.TextField(
        blank=True)
    role = models.CharField(
        max_length=MAX_LEN_ROLE,
        choices=ROLES,
        default=USER)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('pk',)
