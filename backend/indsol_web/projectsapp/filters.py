from django_filters import rest_framework as filters
from projectsapp.models import Adjust, Projects


class AdjustFilter(filters.FilterSet):
    created_at = filters.DateFilter("created_at__date")

    class Meta:
        model = Adjust
        fields = ("contract_id",)


class ProjectsFilter(filters.FilterSet):
    class Meta:
        model = Projects
        fields = ["contract_id"]
