from django.urls import include, path
from newsapp.views import NewsViewSet, MediaViewSet
from rest_framework import routers


# Wiki
news = routers.DefaultRouter()
news.register("list", NewsViewSet, basename="news")
news.register("media", MediaViewSet, basename="media")

urlpatterns = [
    path("", include(news.urls)),
]
