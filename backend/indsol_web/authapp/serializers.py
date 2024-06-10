from authapp.models import Users, Districts, Branches, Clients, Managers
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# Превращают данные модели в JSON


# Сериализация таблицы "Пользователи"
class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "password",
            "is_staff",
            "is_manager",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "is_staff",
            "is_manager",
            "created_at",
            "updated_at",
        ]


class DistrictsSerializers(ModelSerializer):
    class Meta:
        model = Districts
        fields = [
            "id",
            "name",
        ]


class BranchesSerializers(ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            "id",
            "name",
        ]


class ClientsSerializers(ModelSerializer):
    class Meta:
        model = Clients
        fields = [
            "user_id",
            "district_id",
            "branch_id",
            "inn",
            "organization",
            "agreement",
        ]


class ManagersSerializers(ModelSerializer):
    class Meta:
        model = Managers
        fields = [
            "user_id",
            "district_id",
            "branch_id",
        ]
