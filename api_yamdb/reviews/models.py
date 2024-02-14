from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


from reviews.validator import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
        null=False,
        blank=False
    )
    year = models.IntegerField(
        verbose_name='Год произведения',
        validators=(validate_year,)
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        default='-пусто-',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
