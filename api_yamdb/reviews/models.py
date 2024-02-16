from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


from reviews.validator import validate_year

class MyUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        null=False)
    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail',
        unique=True,
        blank=False,
        null=False)
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
        blank=False,
        null=False)


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

class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Значение рейтинга не может быть ниже 1.'),
            MaxValueValidator(10, 'Значение рейтинга не может быть выше 10.')
        ],
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Отзыв {self.author.username} на {self.title.name}'
    
class Comment(models.Model):
    text = models.TextField(verbose_name='text')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарии',
        related_name='comments'
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text