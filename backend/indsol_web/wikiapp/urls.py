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
wiki.register("list", WikiViewSet, basename="wiki") # Список баз знаний
wiki.register("menu", MenuViewSet, basename="menu") # Список разделов меню
wiki.register("sections", SectionsViewSet, basename="sections") # Список подразделов меню
wiki.register("articles", ArticleViewSet, basename="articles") # Список статей
wiki.register("files", FilesViewSet, basename="files") # Список файлов статьи
wiki.register("images", ImagesViewSet, basename="images") # Список изображений статьи
wiki.register("videos", VideosViewSet, basename="videos") # Список видео статьи


urlpatterns = [
    path("", include(wiki.urls)),
]
