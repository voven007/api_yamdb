from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для модели Title."""
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    year = NumberFilter(
        field_name="year",
        lookup_expr="iexact"
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
