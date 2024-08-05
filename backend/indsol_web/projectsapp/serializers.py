from projectsapp.models import Projects#, Contracts
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class ContractsSerializers(ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

class ProjectsSerializer(ModelSerializer):
    contract_number = serializers.CharField(source='contract_id.contract_number')
    class Meta:
        model = Projects
        fields = [
            "contract_id",
            "contract_number",
            "name",
            "start_date",
            "deadline",
            "is_completed",
            "actual_date",
            "responsible",
            "responsible_rp",
        ]
