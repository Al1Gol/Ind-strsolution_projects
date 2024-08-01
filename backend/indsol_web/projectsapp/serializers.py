from projectsapp.models import Projects
from rest_framework.serializers import ModelSerializer


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
