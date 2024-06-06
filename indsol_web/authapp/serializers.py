from authapp.models import Users
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
