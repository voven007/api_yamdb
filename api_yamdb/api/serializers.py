from rest_framework import exceptions, serializers
from rest_framework.generics import get_object_or_404

from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Title, Review
from users.constants import MAX_LEN_EMAIL, MAX_LEN_USERNAME
from users.models import MyUser, ROLES


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    email = serializers.EmailField(
        max_length=MAX_LEN_EMAIL,
        validators=[UniqueValidator(
            queryset=MyUser.objects.all())])
    role = serializers.ChoiceField(
        choices=ROLES,
        required=False)

    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ("role",)

    def validate_username(self, username):
        username = username.lower()
        if username == "me":
            raise serializers.ValidationError(
                'Имя пользователя "me" не доступно для регистрации.')
        return username


class JWTTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(max_length=MAX_LEN_USERNAME)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        if not MyUser.objects.filter(username=data['username']).exists():
            raise exceptions.NotFound(
                'Такого пользователя не существует')
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения произведений."""
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведений."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов на произведения."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'pub_date', 'score')

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        author = self.context['request'].user
        if (self.context['request'].method == 'POST'
           and Review.objects.filter(title=title, author=author).exists()):
            raise serializers.ValidationError(
                "Можно добавить только один отзыв"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')
