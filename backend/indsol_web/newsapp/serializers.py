from newsapp.models import News, Media
from rest_framework.serializers import ModelSerializer


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "text",
            "cover",
            "to_slider",
            "created_at",
            "updated_at",
            "publicated_at",
        ]

    def create(self, validated_data):
        return News.objects.create(**validated_data)


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "news_id", "media"]

    def create(self, validated_data):
        return Media.objects.create(**validated_data)
