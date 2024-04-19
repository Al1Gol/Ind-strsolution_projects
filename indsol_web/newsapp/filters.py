from django_filters import rest_framework as filters
from newsapp.models import Media


class MediaFilter(filters.FilterSet):
    class Meta:
        model = Media
        fields = ["news_id"]
