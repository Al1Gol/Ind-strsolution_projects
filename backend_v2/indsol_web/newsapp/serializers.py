from newsapp.models import News, Media
from rest_framework.serializers import ModelSerializer

# Список новостей
class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        return News.objects.create(**validated_data)

# Список медиа файлов новостей
class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

    def create(self, validated_data):
        return Media.objects.create(**validated_data)
