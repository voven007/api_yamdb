
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets


from api.filters import TitleFilter
from api.mixins import MixinViewSet
from api.permissions import IsAdminOrIsModeratorOrIsUser, IsAdminOrReadOnly
from api.serializers import (
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


class MeView(RetrieveUpdateAPIView):
    pass


class SignupView(CreateAPIView):
    pass


class TokenView(CreateAPIView):
    pass


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
