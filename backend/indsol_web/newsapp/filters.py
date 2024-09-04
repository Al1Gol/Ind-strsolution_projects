from django_filters import rest_framework as filters
from newsapp.models import News, Media


class NewsDateFilter(filters.FilterSet):
    day = filters.CharFilter("created_at__date", lookup_expr='icontains')
    title = filters.CharFilter("title", lookup_expr='icontains')

    model = News
    fields = ["day", "title",]


class MediaFilter(filters.FilterSet):
    class Meta:
        model = Media
        fields = ["news_id"]
