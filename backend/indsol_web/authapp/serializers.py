from authapp.models import Users, Districts, Branches, Clients, Managers
from projectsapp.serializers import ContractsSerializers
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

# Список пользователей
class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "password",
            "email",
            "is_staff",
            "is_client",
            "is_manager",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_staff", "is_client", "is_manager"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True}
        }

# Список регионов
class DistrictsSerializers(ModelSerializer):
    class Meta:
        model = Districts
        fields = "__all__"


# Список производственных отралсей
class BranchesSerializers(ModelSerializer):
    class Meta:
        model = Branches
        fields = "__all__"


# Список клиентов
class ClientsSerializers(ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"


# Список менеджеров
class ManagersSerializers(ModelSerializer):
    class Meta:
        model = Managers
        fields = "__all__"

# Профиль клиента
class ClientProfileSerializer(ModelSerializer):
    user_info = UsersSerializer()
    client_info = ClientsSerializers()
    contracts = ContractsSerializers(many=True)
    class Meta:
        model = Users
        fields = ['user_info', 'client_info', 'contracts']

# Профиль менеджера
class ManagerProfileSerializer(ModelSerializer):
    user_info = UsersSerializer()
    manager_info = ManagersSerializers()
    class Meta:
        model = Users
        fields = ['user_info', 'manager_info']

# Профиль администратора
class AdminProfileSerializer(ModelSerializer):
    user_info = UsersSerializer()
    class Meta:
        model = Users
        fields = ['user_info']

# Отправка данный регистрации менеджерам
class AuthMailSerializers(Serializer):
    organization = serializers.CharField(max_length=400)
    inn = serializers.CharField(max_length=12)
    branch = serializers.IntegerField()
    district = serializers.IntegerField()
    email = serializers.CharField(max_length=200)

# Отправка пользовательских отчетов
class ReportMailSserializers(Serializer):
    organization = serializers.IntegerField(default=None)
    inn = serializers.CharField(max_length=12, default=None)
    text = serializers.CharField(max_length=10000) 