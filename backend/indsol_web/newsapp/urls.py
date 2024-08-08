from django.urls import include, path
from newsapp.views import NewsViewSet, NewsAdminViewSet, MediaViewSet
from rest_framework import routers


# Wiki
news = routers.DefaultRouter()
news.register("list", NewsViewSet, basename="news") # Список пользовательских новостей
news.register("list-admin", NewsAdminViewSet, basename="news-admin") # Список новостей для админки
news.register("media", MediaViewSet, basename="media") # Список медиа файлов новостей

urlpatterns = [
    path("", include(news.urls)),
]
