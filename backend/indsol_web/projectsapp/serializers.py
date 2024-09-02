from projectsapp.models import Projects, Contracts, Adjust, Documents
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# Список договоров
class ContractsSerializers(ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__'

# Список проектов
class ProjectsSerializer(ModelSerializer):
    contract_number = serializers.CharField(source='contract_id.contract_number')
    class Meta:
        model = Projects
        fields = '__all__'

# Список согласований
class AdjustSerializer(ModelSerializer):
    contract_number = serializers.CharField(source='contract_id.contract_number')
    class Meta:
        model = Adjust
        fields = '__all__'

#Список документов прикрепленных к договору
class DocumentsSerializer(ModelSerializer):
    contract_number = serializers.CharField(source='contract_id.contract_number')
    class Meta:
        model = Documents
        fields = '__all__'