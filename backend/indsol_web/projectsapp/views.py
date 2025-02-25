import json
import os

#from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import (
    ProjectsSerializer,
    ContractsSerializers,
    AdjustSerializer,
    DocumentsSerializer,
)
from authapp.models import Users
from projectsapp.models import Projects, Contracts, Adjust, Documents
from projectsapp.filters import ContractsFilter, AdjustFilter, ProjectsFilter, DocumentsFilter
from indsol_web.settings_celery import add_project_task, add_adjust_task
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
# Список договоров
class ContractsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ContractsSerializers
    queryset = Contracts.objects.all()
    filterset_class = ContractsFilter

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
           return Contracts.objects.filter(client_id__user_id=self.request.user.id)
       elif user[0].is_manager or user[0].is_staff:
            return Contracts.objects.all()
       else:
          raise ValidationError(detail='Invalid Params')
       
    def perform_create(self, serializer):
        serializer.save()
        add_project_task.delay(serializer.data["contract_number"])
        add_adjust_task.delay(serializer.data["contract_number"])

    def perform_update(self, serializer):
        instance = serializer.save()
        print(instance)
        print("contract_number")
        add_project_task.delay(self.request.data["contract_number"])
        add_adjust_task.delay(self.request.data["contract_number"])


# Список проектов
class ProjectsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all().order_by('start_date')
    filterset_class = ProjectsFilter

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
           return Projects.objects.filter(contract_id__client_id__user_id=self.request.user.id)
       elif user[0].is_manager or user[0].is_staff:
            return Projects.objects.all()

# Список согласований
class AdjustViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = AdjustSerializer
    queryset = Adjust.objects.all()
    filterset_class = AdjustFilter

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
           return Adjust.objects.filter(contract_id__client_id__user_id=self.request.user.id)
       elif user[0].is_manager or user[0].is_staff:
            return Adjust.objects.all()

#Список документов прикрепленных к договору
class DocumentsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = DocumentsSerializer
    queryset = Documents.objects.all().order_by('id')
    filterset_class = DocumentsFilter

    # Автоматическое заполнение поля name из имени загружаемого файла
    def perform_create(self, serializer):
        serializer.save(name=self.request.FILES['file'])

    def get_queryset(self):
       user = Users.objects.filter(id=self.request.user.id)
       if user[0].is_client:
           return Documents.objects.filter(contract_id__client_id__user_id=self.request.user.id)
       elif user[0].is_manager or user[0].is_staff:
            return Documents.objects.all()
       
# Методы ручной загрузки выгрузкок из 1С по API  
# Пока что отключены за ненадобностью     
'''
class UploadProjectsView(APIView):
    def post(self, request):
        file_objs = request.FILES['file']
        with default_storage.open(f'./parse_data/projects.json', 'wb+') as destination:
            for chunk in file_objs.chunks():
                destination.write(chunk)
        return HttpResponse({'is_save': True})
    
class UploadAdjustView(APIView):
    def post(self, request):
        file_objs = request.FILES['file']
        with default_storage.open(f'./parse_data/adjust.json', 'wb+') as destination:
            for chunk in file_objs.chunks():
                destination.write(chunk)
        return HttpResponse({'is_save': True})
'''

# Методы автоматической загрузки выгрузкок из 1С по API 
#
#  Атоматическая загрузка Проектов
class GetProjectsView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        file_objs = request.data["data"]
        bd = json.loads(file_objs)["BD"]
        path = f'{settings.MEDIA_ROOT}/parse_data'
        if not os.path.exists(path):
            os.makedirs(path)
        if bd == "ST_PROJECT":
            with open(f'{path}/st_projects.json', 'w+', encoding='utf-8') as destination:
                destination.write(str(file_objs))
            return HttpResponse({'is_save': True})
        elif bd == "EXPORT":
            with open(f'{path}/export_projects.json', 'w+', encoding='utf-8') as destination:
                destination.write(str(file_objs))
            return HttpResponse({'is_save': True})
        else:
            with open(f'{path}/unknown_projects.json', 'w+', encoding='utf-8') as destination:
                destination.write(str(file_objs))
            return HttpResponse({'is_save': True})
    
#  Атоматическая загрузка Согласований
class GetAdjustView(APIView):
    def post(self, request):
        file_objs = request.data["data"]
        print(json.loads(file_objs)["BD"])
        bd = json.loads(file_objs)["BD"]
        path = f'{settings.MEDIA_ROOT}/parse_data'
        if not os.path.exists(path):
            os.makedirs(path)
        if bd == "ST_PROJECT":
            with open(f'{path}/st_adjust.json', 'w+', encoding='utf-8') as destination:
                destination.write(str(file_objs))
            return HttpResponse({'is_save': True})
        elif bd == "EXPORT":
            with open(f'{path}/export_adjust.json', 'w+', encoding='utf-8') as destination:
                destination.write(str(file_objs))
            return HttpResponse({'is_save': True})
        else:
            with open(f'{path}/unknown_adjust.json', 'w+', encoding='utf-8') as destination:
                destination.write(str(file_objs))
            return HttpResponse({'is_save': True})
