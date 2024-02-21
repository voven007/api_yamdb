from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = ((USER, 'Аутентифицированный пользователь'),
         (MODERATOR, 'Модератор'),
         (ADMIN, 'Администратор'))


class MyUser(AbstractUser):
    """Модель прользователей"""
    username = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ в имени'
        )]
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False
    )
    first_name = models.CharField("имя", max_length=150, blank=True)
    last_name = models.CharField("фамилия", max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя', max_length=15, choices=ROLES, default=USER)

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