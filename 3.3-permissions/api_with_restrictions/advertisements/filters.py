from django_filters import rest_framework as filters

from advertisements.models import Advertisement
from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementFilter(filters.FilterSet, DjangoFilterBackend):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at']
