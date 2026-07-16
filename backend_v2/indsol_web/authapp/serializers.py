from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError

from authapp.models import (Users, 
                            Districts, 
                            Branches, 
                            Clients, 
                            Managers, 
                            Wiki_Permissions, 
                            Wiki_Group_Permissions)
from projectsapp.serializers import ContractsSerializers


class UsersSerializer(ModelSerializer):
    #groups = serializers.PrimaryKeyRelatedField(
    #    many=True, 
    #    queryset=Group.objects.all(), 
    #    write_only=True
    #)

    # Дополнительно можно выводить группы при чтении (read-only)
    group_id = serializers.SerializerMethodField()
    wiki_group_id = serializers.PrimaryKeyRelatedField(
        queryset=Wiki_Group_Permissions.objects.all(), 
        source='wiki_group'
    )
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
            "group_id",
            "wiki_group_id"
        ]
        #read_only_fields = ["is_staff", "is_client", "is_manager"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True}
        }

    def get_group_id(self, obj):
        get_ids = [group.id for group in obj.groups.all()]
        if len(get_ids) > 0:
            return [group.id for group in obj.groups.all()][0]
        else:
            return 
        
    def create(self, validated_data):        
        # Получаем значение напрямую из сырых данных запроса
        group_id = self.initial_data.get('group_id')
        
        if group_id is not None:
            try:
                group = Group.objects.get(pk=group_id)

            except Group.DoesNotExist:
                raise ValidationError({"group_id": "Группа с таким ID не существует."})
            else:
                user = Users.objects.create_user(**validated_data)
                user.groups.add(group)
        return user

    def update(self, instance, validated_data):
        # Извлекаем переданную группу
        if 'group_id' in self.initial_data:
            group_id = self.initial_data.get('group_id')
            
            # Перезаписываем список групп (оставляем только одну)
            if group_id is not None:
                try:
                    group = Group.objects.get(pk=group_id)
                except:
                    raise ValidationError({"group_id": "Группа с таким ID не существует."}) 
                else:
                    # Обновляем текстовые поля пользователя
                    instance = super().update(instance, validated_data)
                    instance.groups.set([group_id])   
            else:
                instance.groups.clear()
        return instance

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

class ContentTypeSerializer(serializers.ModelSerializer):
    """ Список разрешений (ролевая система) """
    class Meta:
        model = ContentType
        fields = ['app_label', 'model', 'app_labeled_name']

class PermissionSerializer(serializers.ModelSerializer):
    """ Список разрешений (ролевая система) """
    content_type = ContentTypeSerializer()
    title = serializers.SerializerMethodField()
    class Meta:
        model = Permission
        #fields ='__all__'
        fields = ['id', 'name', 'codename', 'title', 'content_type']

    def get_title(self, obj):
        return '{} {} {}'.format(obj.content_type.app_labeled_name, '|', obj.codename) 


class GroupSerializer(serializers.ModelSerializer):
    """ Список групп (ролевая система) """
    class Meta:
        model = Group
        fields ='__all__'


class WikiPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiki_Permissions
        fields ='__all__'


class WikiGroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiki_Group_Permissions
        fields ='__all__'