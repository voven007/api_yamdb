
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )

urlpatterns = [
    path('v1/', include(router.urls))
    path('v1/', include('djoser.urls.jwt')),
]
