import django_filters
from .models import Country, Category



class CountryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='country_name', lookup_expr='icontains', label='Search')

    class Meta:
        model = Country
        fields = ['search']


class CategoryFilter(django_filters.FilterSet):
    country_id = django_filters.NumberFilter(field_name='country__id', label='Country ID')
    search = django_filters.CharFilter(field_name='category_title', lookup_expr='icontains', label='Search')

    class Meta:
        model = Category
        fields = ['country_id', 'search']