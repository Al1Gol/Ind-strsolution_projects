from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import ProjectsSerializer, ContractsSerializers, AdjustSerializer
from projectsapp.models import Projects, Contracts, Adjust


# Договоры
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

# Проекты
class ProjectsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()

# Согласование
class AdjustViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ProjectsSerializer
    queryset = Adjust.objects.all()