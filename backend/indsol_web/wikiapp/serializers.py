from wikiapp.models import Wiki, Articles, Files, Images, Menu, Sections, Videos
from rest_framework.serializers import ModelSerializer

# Список баз знаний
class WikiSerializer(ModelSerializer):
    class Meta:
        model = Wiki
        fields = '__all__'

    def create(self, validated_data):
        return Wiki.objects.create(**validated_data)

# Список разделов меню
class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)

 # Список подразделов меню
class SectionsSerializer(ModelSerializer):

    class Meta:
        model = Sections
        fields = '__all__'

    def create(self, validated_data):
        return Sections.objects.create(**validated_data)

# Список файлов статьи
class FilesSerializer(ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

# Список статей
class ArticlesSerializer(ModelSerializer):
    files = FilesSerializer(many=True, read_only=True)

    class Meta:
        model = Articles

        fields = [
            "id",
            "name",
            "menu_id",
            "section_id",
            "text",
            "files",
            "order",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)

# Список изображений статьи
class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ["img"]

# Список видео статьи
class VideosSerializer(ModelSerializer):
    class Meta:
        model = Videos
        fields = ["video"]
