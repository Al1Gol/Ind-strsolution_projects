from django.urls import include, path
from newsapp.views import NewsViewSet, NewsAdminViewSet, MediaViewSet
from rest_framework import routers


# Wiki
news = routers.DefaultRouter()
news.register("list", NewsViewSet, basename="news")
news.register("admin-list", NewsViewSet, basename="news-admin")
news.register("media", MediaViewSet, basename="media")

urlpatterns = [
    path("", include(news.urls)),
]
