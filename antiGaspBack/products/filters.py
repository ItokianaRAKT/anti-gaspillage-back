import django_filters
from django.utils import timezone
from datetime import timedelta
from math import radians, cos, sin, asin, sqrt
from .models import Product


def haversine(lat1, lon1, lat2, lon2):
    """Distance en km entre deux points GPS."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))


class ProductFilter(django_filters.FilterSet):
    category = django_filters.UUIDFilter(field_name='category__id_category')
    dlc_24h = django_filters.BooleanFilter(method='filter_dlc_24h')
    search = django_filters.CharFilter(field_name='name_product', lookup_expr='icontains')
    is_free = django_filters.BooleanFilter(method='filter_is_free')

    # Filtre distance — paramètres: lat, lng, distance_km
    lat = django_filters.NumberFilter(method='noop')
    lng = django_filters.NumberFilter(method='noop')
    distance_km = django_filters.NumberFilter(method='noop')

    def filter_dlc_24h(self, queryset, name, value):
        if value:
            limit = timezone.localdate() + timedelta(hours=24)
            return queryset.filter(expiration_date__lte=limit)
        return queryset

    def filter_is_free(self, queryset, name, value):
        if value:
            return queryset.filter(price_product=0)
        return queryset.exclude(price_product=0)

    def noop(self, queryset, name, value):
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        lat = self.data.get('lat')
        lng = self.data.get('lng')
        distance_km = self.data.get('distance_km')

        if lat and lng and distance_km:
            try:
                lat, lng, distance_km = float(lat), float(lng), float(distance_km)
                filtered_ids = [
                    p.id_product for p in queryset
                    if p.latitude and p.longitude and
                    haversine(lat, lng, p.latitude, p.longitude) <= distance_km
                ]
                queryset = queryset.filter(id_product__in=filtered_ids)
            except (ValueError, TypeError):
                pass

        return queryset

    class Meta:
        model = Product
        fields = ['category', 'search', 'dlc_24h', 'is_free']