import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.UUIDFilter(field_name='category__id_category')
    dlc_24h = django_filters.BooleanFilter(method='filter_dlc_24h')

    def filter_dlc_24(self, queryset, name, value):
        if value:
            limit = timezone.localdate() + timedelta(hours=24)
            return queryset.filter(expiration_date__lte=limit)
        return queryset
    
    class Meta: 
        model = Product
        fields = ['category']