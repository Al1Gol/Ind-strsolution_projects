from wikiapp.models import Wiki, Articles, Files, Images, Menu, Sections, Videos
from rest_framework.serializers import ModelSerializer


class WikiSerializer(ModelSerializer):
    class Meta:
        model = Wiki
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return Wiki.objects.create(**validated_data)


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "wiki_id",
            "name",
            "img",
            "is_article",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)


class SectionsSerializer(ModelSerializer):

    class Meta:
        model = Sections
        fields = [
            "id",
            "menu_id",
            "name",
            "img",
            "is_article",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return Sections.objects.create(**validated_data)


class FilesSerializer(ModelSerializer):
    class Meta:
        model = Files
        fields = [
            "id",
            "article_id",
            "name",
            "file",
            "created_at",
            "updated_at",
        ]


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
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)


class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ["img"]


class VideosSerializer(ModelSerializer):
    class Meta:
        model = Videos
        fields = ["video"]
