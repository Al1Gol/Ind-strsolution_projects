from django.urls import include, path
from rest_framework import routers

from projectsapp.views import ProjectsViewSet, ContractsViewSet, AdjustViewSet, DocumentsViewSet
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

# /api/v1/projects/
projects = routers.DefaultRouter()
projects.register("list", ProjectsViewSet, basename="projects") # # Список договоров
projects.register("contracts", ContractsViewSet, basename="contracts") # Список проектов
projects.register("adjust", AdjustViewSet, basename="adjust") # Список согласований
projects.register("documents", DocumentsViewSet, basename="documents") # Список документов прикрепленных к договору


urlpatterns = [
    path("", include(projects.urls)),
]
