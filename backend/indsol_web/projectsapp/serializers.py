from projectsapp.models import Projects, Contracts
from rest_framework.serializers import ModelSerializer


class ContractsSerializers(ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__'

class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = [
            "contract_id",
            "name",
            "start_date",
            "deadline",
            "is_completed",
            "actual_date",
            "responsible",
            "responsible_rp",
        ]
