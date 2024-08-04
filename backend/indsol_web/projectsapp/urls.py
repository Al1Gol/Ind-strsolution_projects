from django.urls import include, path
from rest_framework import routers

from projectsapp.views import ProjectsViewSet, ContractsViewSet
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

projects = routers.DefaultRouter()
projects.register("list", ProjectsViewSet, basename="projects")
projects.register("contracts", ContractsViewSet, basename="contracts")


urlpatterns = [
    path("", include(projects.urls)),
]
