from authapp.views import ProfileViewSet, UsersViewSet
from django.contrib import admin
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
from rest_framework.authtoken import views
from rest_framework_simplejwt import views as jwt_views

auth = routers.DefaultRouter()
auth.register("users", UsersViewSet, basename="users")
auth.register("profile", ProfileViewSet, basename="profile")
# Wiki
wiki = routers.DefaultRouter(trailing_slash=False)
wiki.register("main/", WikiViewSet, basename="wiki")
wiki.register("menu/", MenuViewSet, basename="menu")
wiki.register("sections/", SectionsViewSet, basename="sections")
wiki.register("articles/", ArticleViewSet, basename="articles")
wiki.register("files/", FilesViewSet, basename="files")
wiki.register("images/", ImagesViewSet, basename="images")
wiki.register("videos/", VideosViewSet, basename="videos")


urlpatterns = [
    path("api/v1/", include(auth.urls)),
    path("api/v1/wiki/", include(wiki.urls)),
    path("api/v1/auth/", include("rest_framework.urls")),
    path(
        "api/v1/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
