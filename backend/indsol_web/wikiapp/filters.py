from django_filters import rest_framework as filters
from wikiapp.models import Articles, Files, Sections, Menu


class MenuFilter(filters.FilterSet):
    class Meta:
        model = Menu
        fields = ["wiki_id"]


class SectionsFilter(filters.FilterSet):
    class Meta:
        model = Sections
        fields = ["menu_id"]


class FilesFilter(filters.FilterSet):
    class Meta:
        model = Files
        fields = ["article_id"]


class ArticlesFilter(filters.FilterSet):
    class Meta:
        model = Articles
        fields = ["menu_id", "section_id"]
