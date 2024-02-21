from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


from api.filters import TitleFilter
from api.mixins import MixinViewSet
from api.permissions import (
    IsAdmin,
    IsAdminOrIsModeratorOrIsUser,
    IsAdminOrReadOnly
)
from .serializers import (
    AdminSerializer,
    JWTTokenSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    CommentSerializer,
    ReviewSerializer
)
from api.utils import send_confirmation_code_on_email
from reviews.models import Category, Genre, Title, Review

from users.models import MyUser


class SignUp(APIView):
    """Вьюкласс для регистрации пользователей"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user = MyUser.objects.filter(
            username=request.data.get("username"),
            email=request.data.get("email")
        ).first()

        if user:
            send_confirmation_code_on_email(user.username, user.email)

            return Response(status=status.HTTP_200_OK)

        if serializer.is_valid():
            try:
                MyUser.objects.get_or_create(
                    username=serializer.data.get('username'),
                    email=serializer.data.get('email'))
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            send_confirmation_code_on_email(
                serializer.data['username'], serializer.data['email'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    """Вьюкласс для получения токена"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                MyUser, username=serializer.data['username'])
            if default_token_generator.check_token(
               user, serializer.data['confirmation_code']):
                token = AccessToken.for_user(user)

                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK)

            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы админа с пользователями"""

    queryset = MyUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch', ]

    @action(detail=False, methods=('get', 'patch'),
            url_name='me', permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = AdminSerializer(
            request.user,
            data=request.data,
            partial=True)
        if serializer.is_valid():
            serializer.save(role=self.request.user.role)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(MixinViewSet):
    """ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(MixinViewSet):
    """ViewSet для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrIsModeratorOrIsUser,)
    http_method_names = ['get', 'post', 'delete', 'patch', ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrIsModeratorOrIsUser,)
    http_method_names = ['get', 'post', 'delete', 'patch', ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            msg = {"error": f'Метод {request.method} не доступен.'}
            return Response(
                data=msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)