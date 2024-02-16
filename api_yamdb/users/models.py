from django.contrib.auth.models import AbstractUser
from django.db import models
# from django import forms


class MyUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,)
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
