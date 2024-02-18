from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLES = [
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор')
]


class MyUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )])
    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail',
        unique=True,)
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True)
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True)
    role = models.CharField(
        max_length=150,
        verbose_name='Роль',
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
