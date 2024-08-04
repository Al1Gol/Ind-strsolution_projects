from newsapp.models import News, Media
from rest_framework.serializers import ModelSerializer


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        return News.objects.create(**validated_data)


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

    def create(self, validated_data):
        return Media.objects.create(**validated_data)
