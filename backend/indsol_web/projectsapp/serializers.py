from projectsapp.models import Projects, Contracts, Adjust
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# Контракты
class ContractsSerializers(ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__'

# Проекты
class ProjectsSerializer(ModelSerializer):
    contract_number = serializers.CharField(source='contract_id.contract_number')
    class Meta:
        model = Projects
        fields = '__all__'

# Согласование
class AdjustSerializer(ModelSerializer):
    class Meta:
        model = Adjust
        fields = '__all__'