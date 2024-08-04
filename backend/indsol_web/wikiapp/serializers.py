from wikiapp.models import Wiki, Articles, Files, Images, Menu, Sections, Videos
from rest_framework.serializers import ModelSerializer


class WikiSerializer(ModelSerializer):
    class Meta:
        model = Wiki
        fields = '__all__'

    def create(self, validated_data):
        return Wiki.objects.create(**validated_data)


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)


class SectionsSerializer(ModelSerializer):

    class Meta:
        model = Sections
        fields = '__all__'

    def create(self, validated_data):
        return Sections.objects.create(**validated_data)


class FilesSerializer(ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


class ArticlesSerializer(ModelSerializer):
    files = FilesSerializer(many=True, read_only=True)

    class Meta:
        model = Articles

        fields = '__all__'

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
