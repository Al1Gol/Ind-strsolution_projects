import logging
from authapp.models import Users, Districts, Branches, Clients, Managers
from authapp.serializers import (
    ProfileSerializer,
    UsersSerializer,
    DistrictsSerializers,
    BranchesSerializers,
    ClientsSerializers,
    ManagersSerializers,
)
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import AllowAny
from indsol_web.permissions import AdminUserOrAuthReadOnly


# Список пользователей
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


# Профиль текущего пользователя
class ProfileViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = Users.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(username=self.request.user)
        return self.request


# Список регионов
class DistrictsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Districts.objects.all()
    serializer_class = DistrictsSerializers
    permission_classes = [AllowAny]

# Список производственных отралсей
class BranchesViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializers

# Список клиентов
class ClientsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializers

# Список менеджеров
class ManagersViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Managers.objects.all()
    serializer_class = ManagersSerializers


# Пинг доступности бэкенда
class PingViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response()
