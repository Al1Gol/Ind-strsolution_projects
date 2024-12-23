import json
import os

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

class GetProjectsView(APIView):
    def post(self, request):
        file_objs = request.data["data"]
        path = f'{settings.MEDIA_ROOT}/parse_data'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}/projects.json', 'w+', encoding='utf-8') as destination:
            destination.write(json.dumps(file_objs, ensure_ascii=False))
        return HttpResponse({'is_save': True})
    
class GetAdjustView(APIView):
    def post(self, request):
        file_objs = request.data["data"]
        path = f'{settings.MEDIA_ROOT}/parse_data'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}/adjust.json', 'w+', encoding='utf-8') as destination:
            destination.write(json.dumps(file_objs, ensure_ascii=False))
        return HttpResponse({'is_save': True})