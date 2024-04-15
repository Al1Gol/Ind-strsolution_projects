from django.urls import include, path
from newsapp.views import NewsView, MediaView
from rest_framework import routers


# Wiki
wiki = routers.DefaultRouter()
wiki.register("", NewsView, basename="news")
wiki.register("media/", MediaView, basename="media")

urlpatterns = [
    path("", include(wiki.urls)),
]
