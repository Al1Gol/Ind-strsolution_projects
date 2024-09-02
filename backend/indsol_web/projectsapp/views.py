from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import (
    ProjectsSerializer,
    ContractsSerializers,
    AdjustSerializer,
    DocumentsSerializer,
)
from projectsapp.models import Projects, Contracts, Adjust, Documents
from projectsapp.filters import ContractsFilter, AdjustFilter, ProjectsFilter, DocumentsFilter


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
    filterset_class = ContractsFilter


# Список проектов
class ProjectsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all().order_by('start_date')
    filterset_class = ProjectsFilter


# Список согласований
class AdjustViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = AdjustSerializer
    queryset = Adjust.objects.all()
    filterset_class = AdjustFilter

#Список документов прикрепленных к договору
class DocumentsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = DocumentsSerializer
    queryset = Documents.objects.all().order_by('id')
    filterset_class = DocumentsFilter