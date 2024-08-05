from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import ProjectsSerializer, ContractsSerializers
from projectsapp.models import Projects, Contracts


# Create your views here.
class ContractsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Contracts.objects.all()
    serializer_class = ContractsSerializers

class ProjectsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):

    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
