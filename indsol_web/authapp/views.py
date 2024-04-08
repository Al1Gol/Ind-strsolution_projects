import logging
from authapp.models import Departments, Users
from authapp.serializers import (
    DepartmentsSerializer,
    ProfileSerializer,
    UsersSerializer,
)
from django.contrib.auth.hashers import make_password
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from ipm_knowledge.permissions import AdminUserOrAuthReadOnly


class DepartmentsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = DepartmentsSerializer
    queryset = Departments.objects.all().order_by("created_at")
    permission_classes = [AdminUserOrAuthReadOnly]


class UsersViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = UsersSerializer

    queryset = Users.objects.all().order_by("created_at")
    permission_classes = [AdminUserOrAuthReadOnly]

    def perform_create(self, serializer):
        # Устанавливаем хэширование пароля
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Устанавливаем хэширование пароля
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()


class ProfileViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = Users.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.action == "list":
            print(self.request.user)
            return self.queryset.filter(username=self.request.user)
        return self.request
