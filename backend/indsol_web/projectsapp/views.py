from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import ProjectsSerializer
from projectsapp.models import Projects


# Create your views here.
class ProjectsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):

    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
