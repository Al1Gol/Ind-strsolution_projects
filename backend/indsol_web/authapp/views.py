import logging
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.core.mail import send_mail
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django.contrib.auth.base_user import BaseUserManager

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
    AdminProfileSerializer,
    ReportMailSserializers,
    GenerateNewPasswordSerializer
)
from authapp.filters import ClientFilter, ManagerFilter

from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins, ViewSet
from rest_framework.permissions import AllowAny
from indsol_web.permissions import *



def reg_mail_body(request):
     branch = Branches.objects.get(id=request.data["branch"])
     district = Districts.objects.get(id=request.data["district"])
     return   f'Заявка на регистрацию на портале ipm-portal.\n\n \
                Наименование организации: {request.data["organization"]};\n \
                ИНН: {request.data["inn"]};\n \
                Регион: {district.name};\n \
                Отрасль: {branch.name};\n \
                Почта: {request.data["email"]};'


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

# Список пользователей
class GenerateNewPasswordViewSet(
    GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = Users.objects.all()
    serializer_class = GenerateNewPasswordSerializer
    permission_classes = [ModerateAndAdminUpdate]

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated and (request.user.is_manager or request.user.is_admin):
            user = self.get_object()
            if (user.is_client):
                password = BaseUserManager().make_random_password()
                user_obj = Users.objects.get(id=user.id)
                db_password = make_password(password) 
                user_obj.password = db_password
                user_obj.save()
                print(db_password)
                print(password)
                send_body = f'Данные для авторизации: \n\n\
                    Логин: {user.username}, \n\
                    Пароль: {password}'
                send_mail(
                        f"Восстановление доступа - ipm-portal.ru", # Тема
                        send_body, # Тело запроса
                        "info@ipm-portal.ru", # Почта отправителя  
                        [user_obj.email], # Почта получателей
                    ) # Отправка mail
                return Response({'status': 'Пароль изменен. Сведения об авторизации направлены на почту.'})
            else:
                return Response({"error": 'Указанный пользователь не является клиентом.'},
                                status=status.HTTP_403_FORBIDDEN)
        return Response({"error": 'Пользователь не авторизован, либо не хватет прав доступа'},
                                status=status.HTTP_401_UNAUTHORIZED)

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
    permission_classes = [AllowAny]


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
    # При создании экземляра Клиенты соответсвующему Пользователю устаналивается True в поле is_client
    def perform_create(self, serializer):
        get_data = ClientsSerializers(data=self.request.data)
        get_data.is_valid()   
        user=Users.objects.get(id=get_data.data["user_id"])
        if get_data.is_valid():
            user.is_client=True   
            serializer.save()     
            user.save()

    # При удалении экземляра Клиенты соответсвующему Пользователю устаналивается False в поле is_client
    def perform_destroy(self, instance):
        user=Users.objects.get(id=instance.user_id_id)
        user.is_client=False  
        user.save()
        instance.delete()


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
    
    # При удалении экземляра Менеджеры соответсвующему Пользователю устаналивается False в поле is_client
    def perform_destroy(self, instance):
        user=Users.objects.get(id=instance.user_id_id)
        user.is_manager=False  
        user.save()
        instance.delete()


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


# Отправка данных регистрации менеджерам
@api_view(["POST"])
@permission_classes([AllowAny])
def AuthMailView(request):
    if request.method == "POST":
        auth_mail_serializer = AuthMailSerializers(data=request.data)
        if auth_mail_serializer.is_valid():
            managers = Managers.objects.filter(branch_id__id=request.data["branch"]) # Список менеджеров по выбранной отрасли
            emails = [Users.objects.get(id=manager.user_id_id).email for manager in managers] # Список email менеджеров по выбранной отрасли
            emails.append("ruktp@promreshenie.ru")
            send_mail(
                f"Заявка на регистрацию {request.data['organization']} ИНН {request.data['inn']}", # Тема
                reg_mail_body(request), # Тело запроса
                "info@ipm-portal.ru", # Почта отправителя
                emails, # Почта получателей

            )
            return Response({'send': True, 'managers':emails})
        else:                                                         
            return Response({'send': False, 'error': 'Некорректно заполнены сведения'})  # Некорретные данные запроса
    return Response({'send': False, 'error': 'unknown'})

# Отправка пользовательского обращения
@api_view(["POST"])
def ReportMailView(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id) # Текущий пользователь
        #client = Clients.objects.get(user_id=user.id) # Текущая организация
        send_body = f'Данные пользователя: \n\n\
                 Тип учетной записи: Менеджер, \n\
                 Логин: {user.username}, \n\
                 Почта: {user.email}, \n\n\
                 Сообщение: \n\
                 {request.data["text"]}'
        send_mail(
                f"Обращение. {user.username} email {user.email}", # Тема
                send_body, # Тело запроса
                "info@ipm-portal.ru", # Почта отправителя  
                ["ruktp@promreshenie.ru", "ipm-support@promreshenie.ru"], # Почта получателей
            ) # Отправка mail
        return Response({'send': True})
    return Response({'send': False})
