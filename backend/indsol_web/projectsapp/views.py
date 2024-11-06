from rest_framework.viewsets import GenericViewSet, mixins
from projectsapp.serializers import (
    ProjectsSerializer,
    ContractsSerializers,
    AdjustSerializer,
    DocumentsSerializer,
    UploadProjectsSerializer
)
from authapp.models import Users
from projectsapp.models import Projects, Contracts, Adjust, Documents
from projectsapp.filters import ContractsFilter, AdjustFilter, ProjectsFilter, DocumentsFilter
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
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
        print(request)
        serializer = UploadProjectsSerializer(request)
        print(serializer.data)
    
'''       
class UploadProjectsView(APU):
    serializer_class = UploadProjectsSerializer

    def create(self, request, *args, **kwargs):
        print(request.data['file'])
        serializer = UploadProjectsSerializer(request)
    print(serializer.data)
        return HttpResponse('')
    '''
# Отправка пользовательского обращения
#@api_view(["POST"])
#def UploadProjectsView(request):
#    print(request.data['file'])
#    serializer = UploadProjectsSerializer(request)
#    print(serializer.data)
#    return Response({'send': False})