from django.urls import include, path
from rest_framework import routers

from projectsapp.views import ProjectsViewSet
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

projects = routers.DefaultRouter()
projects.register("", ProjectsViewSet, basename="projects")


urlpatterns = [
    path("", include(projects.urls)),
    path("debug/", include("rest_framework.urls")),
]
