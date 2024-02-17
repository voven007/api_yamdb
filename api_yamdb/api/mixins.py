from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters, status
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly


class MixinViewSet(ListCreateAPIView,
                   DestroyAPIView,
                   GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = ('slug',)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
