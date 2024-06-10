from django.urls import include, path, re_path
from wikiapp.views import (
    WikiViewSet,
    ArticleViewSet,
    FilesViewSet,
    ImagesViewSet,
    MenuViewSet,
    SectionsViewSet,
    VideosViewSet,
)
from rest_framework import routers


# Wiki
wiki = routers.DefaultRouter()
wiki.register("list", WikiViewSet, basename="wiki")
wiki.register("menu", MenuViewSet, basename="menu")
wiki.register("sections", SectionsViewSet, basename="sections")
wiki.register("articles", ArticleViewSet, basename="articles")
wiki.register("files", FilesViewSet, basename="files")
wiki.register("images", ImagesViewSet, basename="images")
wiki.register("videos", VideosViewSet, basename="videos")


urlpatterns = [
    path("", include(wiki.urls)),
]
