from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


# ENUM_CHOICES = [
#     'user',
#     'moderator',
#     'admin',
# ]


class MyUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        blank=True)
    email = models.CharField(
        max_length=254,
        verbose_name='E-mail',
        blank=True)
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        null=True,
        blank=True)
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        null=True,
        blank=True)
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True)
    role = models.CharField(
        max_length=150,
        verbose_name='Роль',
        blank=True,)

# widget=forms.Select(
#             choices=ENUM_CHOICES)
