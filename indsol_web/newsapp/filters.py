from django_filters import rest_framework as filters
from newsapp.models import News, Media


class NewsDateFilter(filters.FilterSet):
    created_at = filters.DateFilter("created_at__date")
    print(created_at)

    class Meta:
        model = News
        fields = ("created_at",)


class MediaFilter(filters.FilterSet):
    class Meta:
        model = Media
        fields = ["news_id"]
