from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import (
    ProjectsSerializer,
    ContractsSerializers,
    AdjustSerializer,
)
from projectsapp.models import Projects, Contracts, Adjust
from projectsapp.filters import AdjustFilter, ProjectsFilter


# Список договоров
class ContractsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ContractsSerializers
    queryset = Contracts.objects.all()


# Список проектов
class ProjectsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
    filterset_class = ProjectsFilter


# Список согласований
class AdjustViewSet(
    GenericViewSet,
):
    serializer_class = AdjustSerializer
    queryset = Adjust.objects.all()
    filterset_class = AdjustFilter
