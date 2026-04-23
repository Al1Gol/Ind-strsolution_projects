from authapp.models import Users, Districts, Branches, Clients, Managers
from projectsapp.serializers import ContractsSerializers
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import Group, Permission


class UsersSerializer(ModelSerializer):
    """Список пользователей"""
    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_client",
            "is_manager",
            "created_at",
            "updated_at",
        ]
        #read_only_fields = ["is_staff", "is_client", "is_manager"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True}
        }


class GenerateNewPasswordSerializer(ModelSerializer):
    """Генерация нового пароля"""
    class Meta:
        model = Users
        fields = [
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class DistrictsSerializers(ModelSerializer):
    """Список регионов"""
    class Meta:
        model = Districts
        fields = "__all__"



class BranchesSerializers(ModelSerializer):
    """Список производственных отралсей"""
    class Meta:
        model = Branches
        fields = "__all__"



class ClientsSerializers(ModelSerializer):
    """Список клиентов"""
    class Meta:
        model = Clients
        fields = "__all__"


# Список менеджеров
class ManagersSerializers(ModelSerializer):
    class Meta:
        model = Managers
        fields = "__all__"


class ClientProfileSerializer(ModelSerializer):
    """Профиль клиента"""
    user_info = UsersSerializer()
    client_info = ClientsSerializers()
    contracts = ContractsSerializers(many=True)
    class Meta:
        model = Users
        fields = ['user_info', 'client_info', 'contracts']


class ManagerProfileSerializer(ModelSerializer):
    """Профиль менеджера"""
    user_info = UsersSerializer()
    manager_info = ManagersSerializers()
    class Meta:
        model = Users
        fields = ['user_info', 'manager_info']


class AdminProfileSerializer(ModelSerializer):
    """Профиль администратора"""
    user_info = UsersSerializer()
    class Meta:
        model = Users
        fields = ['user_info']


class AuthMailSerializers(Serializer):
    """Отправка данных регистрации менеджерам"""
    organization = serializers.CharField(max_length=400)
    inn = serializers.CharField(max_length=12)
    branch = serializers.IntegerField()
    district = serializers.IntegerField()
    email = serializers.CharField(max_length=200)


class ReportMailSserializers(Serializer):
    """Отправка пользовательских отчетов"""
    organization = serializers.IntegerField(default=None)
    inn = serializers.CharField(max_length=12, default=None)
    text = serializers.CharField(max_length=10000) 

class PermissionSerializer(serializers.ModelSerializer):
    """ Список разрешений (ролевая система) """
    class Meta:
        model = Permission
        fields ='__all__'

class GroupSerializer(serializers.ModelSerializer):
    """ Список групп (ролевая система) """
    class Meta:
            model = Group
            fields ='__all__'