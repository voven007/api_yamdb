
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status


from api.filters import TitleFilter
from api.mixins import MixinViewSet
from api.permissions import (
    IsAdmin,
    IsAdminOrIsModeratorOrIsUser,
    IsAdminOrReadOnly
)
from api.serializers import (
    UserSerializer,
    UserMeSerializer,
    TokenSerializer,
    SignupSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    CommentSerializer,
    ReviewSerializer
)
from reviews.models import Category, Genre, Title, Review

from users.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ["get", "patch", "post", "delete"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )


class MeView(RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        email = request.data.get("email")
        username = request.data.get("username")
        user = MyUser.objects.filter(username=username, email=email).exists()
        if serializer.is_valid() or user:
            user, created = MyUser.objects.get_or_create(
                username=username, email=email
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                "Confirm your registration",
                f"Your confirmation code is: {confirmation_code}",
                None,
                [email],
                fail_silently=False,
            )
            return Response(
                {"email": email, "username": username},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        confirmation_code = request.data.get("confirmation_code")
        username = request.data.get("username")
        if not username or not confirmation_code:
            return Response(
                {"error": "Username and confirmation code are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not MyUser.objects.filter(username=username).exists():
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if serializer.is_valid():
            user = MyUser.objects.get(username=username)
            if default_token_generator.check_token(user, confirmation_code):
                token = RefreshToken.for_user(user)
                return Response(
                    {"token": str(token.access_token)},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid confirmation code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
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

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrIsModeratorOrIsUser,)

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