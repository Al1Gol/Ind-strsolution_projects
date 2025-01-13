from django.contrib import admin
from projectsapp.models import Contracts

# Register your models here.
class ContractsAdmin(admin.ModelAdmin):
    fields = ("contract_number")
    list_display = ("contract_number")
    list_display_links = ("contract_number")
    search_fields = (
        "contract_number",
    )


admin.site.register(ContractsAdmin)