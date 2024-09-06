from django_filters import rest_framework as filters
from newsapp.models import News, Media


class NewsDateFilter(filters.FilterSet):
    created_at = filters.CharFilter("created_at__date", lookup_expr='icontains')
    publicated_at = filters.CharFilter("publicated_at__date", lookup_expr='icontains')
    title = filters.CharFilter("title", lookup_expr='icontains')

    model = News
    fields = ["created_at", "publicated_at", "title",]


class MediaFilter(filters.FilterSet):
    class Meta:
        model = Media
        fields = ["news_id"]
