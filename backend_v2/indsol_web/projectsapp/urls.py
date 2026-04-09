from django.urls import include, path
from rest_framework import routers

from projectsapp.views import ProjectsViewSet, ContractsViewSet, AdjustViewSet, DocumentsViewSet, GetProjectsView, GetAdjustView #, UploadProjectsView, UploadAdjustView
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

# /api/v1/projects/
projects = routers.DefaultRouter()
projects.register("list", ProjectsViewSet, basename="projects") # # Список договоров
projects.register("contracts", ContractsViewSet, basename="contracts") # Список проектов
projects.register("adjust", AdjustViewSet, basename="adjust") # Список согласований
projects.register("documents", DocumentsViewSet, basename="documents") # Список документов прикрепленных к договору
#projects.register("upload_projects", UploadProjectsView, basename="upload_projects") # Загрузка файла выгрузки проектов

urlpatterns = [
    path("", include(projects.urls)),
    #path(
    #    "upload_projects/", UploadProjectsView.as_view(), name="upload_projects"
    #),  # Загрузка файла выгрузки Проектов из 1С (временно отключена за ненадобностью)
    #path(
    #    "upload_adjust/", UploadAdjustView.as_view(), name="upload_adjust"
    #),  # Загрузка файла выгрузки Согласований из 1С (временно отключена за ненадобностью)
    path(
        "get_projects/", GetProjectsView.as_view(), name="get_projects"
    ),  # Загрузка файла выгрузки Проектов из 1С
    path(
        "get_adjust/", GetAdjustView.as_view(), name="get_adjust"
    ),  # Загрузка файла выгрузки Согласований из 1С
]
