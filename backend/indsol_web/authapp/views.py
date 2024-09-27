import logging
from django.core.mail import send_mail
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from authapp.models import Users, Districts, Branches, Clients, Managers
from projectsapp.models import Contracts
from authapp.serializers import (
    AuthMailSerializers,
    UsersSerializer,
    DistrictsSerializers,
    BranchesSerializers,
    ClientsSerializers,
    ManagersSerializers,
    ClientProfileSerializer,
    ManagerProfileSerializer,
    AdminProfileSerializer
)
from authapp.filters import ClientFilter, ManagerFilter

from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins, ViewSet
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

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
            return Users.objects.filter(id=self.request.user.id)
       elif user[0].is_manager or user[0].is_staff:
            return Users.objects.all()


# Профиль текущего пользователя
class ProfileViewSet(GenericViewSet, mixins.ListModelMixin,):
    def list(self, request, *args, **kwargs):
        user = Users.objects.filter(id=self.request.user.id)
        profile = {}
        # Обработчик для клиента
        if user[0].is_client:
            profile['user_info'] = Users.objects.get(id=self.request.user.id)
            profile['client_info'] = Clients.objects.get(user_id=self.request.user.id)
            profile['contracts'] = Contracts.objects.filter(client_id__user_id=self.request.user.id)
            serializer = ClientProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Обработчик для менеджера
        elif user[0].is_manager:
            profile['user_info'] = Users.objects.get(id=self.request.user.id)
            profile['manager_info'] = Managers.objects.get(user_id=self.request.user.id)
            serializer = ManagerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Обработчик для админа
        elif user[0].is_staff:
            profile['user_info'] = Users.objects.get(id=self.request.user.id)
            serializer = AdminProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)


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
    filterset_class = ClientFilter

    # Дополнительный обработчик создания экземпляра Мендежеров
    # При создании экземляра Клиенты соответсвующему Пользователю устаналивается флаг True в поле is_client
    def perform_create(self, serializer):
        get_data = ClientsSerializers(data=self.request.data)
        get_data.is_valid()   
        user=Users.objects.get(id=get_data.data["user_id"])
        if get_data.is_valid():
            user.is_client=True   
            serializer.save()     
            user.save()

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
            return Clients.objects.filter(user_id=user[0].id)
       elif user[0].is_manager or user[0].is_staff:
            return Clients.objects.all()

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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['user_id']

    # Дополнительный обработчик создания экземпляра Мендежеров
    # При создании экземляра Менеджеры соответсвующему Пользователю устаналивается флаг True в поле is_manager
    def perform_create(self, serializer):
        get_data = ManagersSerializers(data=self.request.data)
        get_data.is_valid()
        user = Users.objects.get(id=get_data.data["user_id"])
        if get_data.is_valid():
            user.is_manager=True
            serializer.save()    
            user.save()

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
            return Managers.objects.all()
       elif user[0].is_manager or user[0].is_staff:
            return Managers.objects.all()

# Пинг доступности бэкенда
class PingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response()


# Отправка данный регистрации менеджерам
@api_view(["POST"])
@permission_classes([AllowAny])
def AuthMailView(request):
    if request.method == "POST":
        auth_mail_serializer = AuthMailSerializers(data=request.data)
        if auth_mail_serializer.is_valid():
            send_mail(
                "111",
                "111",
                "111",
                ["al1working@mail.ru"],
            )
        return Response()
    return Response()
