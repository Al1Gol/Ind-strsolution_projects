from django_filters import rest_framework as filters
from authapp.models import Clients, Managers

class ClientFilter(filters.FilterSet):
    class Meta:
        model = Clients
        fields = ["user_id", "branch_id", "district_id"]

class ManagerFilter(filters.FilterSet):
    class Meta:
        model = Managers
        fields = ["user_id", "branch_id", "district_id"]

