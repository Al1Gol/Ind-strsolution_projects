from django.contrib import admin
from newsapp.models import News, Media


# Register your models here.
# News
class NewsAdmin(admin.ModelAdmin):
    fields = ("title", "text")
    list_display = ("id", "title", "text", "created_at", "updated_at")
    list_display_links = ("id", "title", "text", "created_at", "updated_at")
    search_fields = (
        "title",
        "created_at",
    )


admin.site.register(News, NewsAdmin)
