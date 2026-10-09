from django.db import transaction
from wikiapp.models import Wiki, Articles, Files, Images, Menu, Sections, Videos
from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, ListField, ValidationError

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
        fields = '__all__'

# Список видео статьи
class VideosSerializer(ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'

class MediaAttachSerializer(Serializer):
    article_id = IntegerField(required=True)
    image_ids = ListField(
        child=IntegerField(), 
        required=False, 
        default=list
    )
    video_ids = ListField(
        child=IntegerField(), 
        required=False, 
        default=list
    )

    def validate_article_id(self, value):
        # Проверяем, существует ли статья
        if not Articles.objects.filter(id=value).exists():
            raise ValidationError("Статья с указанным ID не найдена.")
        return value

    def validate_article_id(self, value):
        if not Articles.objects.filter(id=value).exists():
            raise ValidationError("Статья с таким ID не найдена.")
        return value

    def save(self, **kwargs):
        article_id = self.validated_data['article_id']
        requested_images = set(self.validated_data['image_ids'])
        requested_videos = set(self.validated_data['video_ids'])

        missing_images = []
        missing_videos = []

        with transaction.atomic():
            # Получаем объект статьи, к которой будем привязывать
            article = Articles.objects.get(id=article_id)

            # 1. Привязываем Статью к Изображениям
            if requested_images:
                # Находим только те изображения, которые реально существуют в БД
                existing_images_queryset = Images.objects.filter(id__in=requested_images)
                existing_image_ids = set(existing_images_queryset.values_list('id', flat=True))
                
                # Вычисляем отсутствующие ID изображений
                missing_images = list(requested_images - existing_image_ids)
                
                # Обновляем поле article у существующих изображений одним SQL-запросом
                if existing_image_ids:
                    existing_images_queryset.update(article=article)

            # 2. Привязываем Статью к Видео
            if requested_videos:
                # Находим только те видео, которые реально существуют в БД
                existing_videos_queryset = Videos.objects.filter(id__in=requested_videos)
                existing_video_ids = set(existing_videos_queryset.values_list('id', flat=True))
                
                # Вычисляем отсутствующие ID видео
                missing_videos = list(requested_videos - existing_video_ids)

                # Обновляем поле article у существующих видео одним SQL-запросом
                if existing_video_ids:
                    existing_videos_queryset.update(article=article)

        # Передаем информацию об отсутствующих медиафайлах в контекст сериализатора
        self.context['warnings'] = {
            "missing_image_ids": missing_images,
            "missing_video_ids": missing_videos
        }

        return article