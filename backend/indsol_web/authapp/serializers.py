from authapp.models import Users, Districts, Branches, Clients, Managers
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

# Превращают данные модели в JSON


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
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True}
        }


# Профиль текущего пользователя
class ProfileSerializer(ModelSerializer):
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


# Отправка данный реггистрации менеджерам
class AuthMailSerializers(Serializer):
    organization = serializers.CharField(max_length=400)
    inn = serializers.CharField(max_length=12)
    branch = serializers.IntegerField()
    district = serializers.IntegerField()
    email = serializers.CharField(max_length=200)
