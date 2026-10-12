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
        errors = []

        with transaction.atomic():
            # Получаем объект статьи, к которой будем привязывать
            article = Articles.objects.get(id=article_id)

            # 1. Привязываем Статью к Изображениям
            if requested_images:
                # Находим только те изображения, которые реально существуют в БД
                existing_images_queryset = Images.objects.filter(id__in=requested_images)
                existing_image_ids = set(existing_images_queryset.values_list('id', flat=True))

                # Находим только те изображения, которые не имеют привязки с статье
                unattach_images_queryset  = existing_images_queryset.filter(article_id=None)

                # Находим только те изображения, которые уже имеют привязку с статье
                prev_attach_images_queryset  = existing_images_queryset.exclude(article_id=None)
                prev_attach_images_ids = set(prev_attach_images_queryset.values_list('id', flat=True))
                
                # Вычисляем отсутствующие ID изображений
                missing_images = list(requested_images - existing_image_ids - prev_attach_images_ids)
                
                # Обновляем поле article у существующих изображений одним SQL-запросом
                if unattach_images_queryset.exists():
                    unattach_images_queryset.update(article=article)

                for obj in prev_attach_images_queryset:
                    file_name = obj.img.name.replace("wiki/articles/img/", "")
                    prev_attach_dict = {
                       "image_id": obj.id,
                       "file_name":  file_name,
                       "error": f"Изображение {file_name} уже привязано к другой статье"
                    }
                    errors.append(prev_attach_dict)

            # 2. Привязываем Статью к Видео
            if requested_videos:
                # Находим только те видео, которые реально существуют в БД
                existing_videos_queryset = Videos.objects.filter(id__in=requested_videos)
                existing_video_ids = set(existing_videos_queryset.values_list('id', flat=True))

                # Находим только те видео, которые не имеют привязки с статье
                unattach_videos_queryset  = existing_videos_queryset.filter(article_id=None)

                 # Находим только те видео, которые уже имеют привязку с статье
                prev_attach_videos_queryset  = existing_videos_queryset.exclude(article_id=None)
                prev_attach_videos_ids = set(prev_attach_videos_queryset.values_list('id', flat=True))

                # Вычисляем отсутствующие ID видео
                missing_videos = list(requested_videos - existing_video_ids - prev_attach_videos_ids)

                # Обновляем поле article у существующих видео одним SQL-запросом
                if existing_video_ids:
                    unattach_videos_queryset.update(article=article)

                for obj in prev_attach_videos_queryset:
                    file_name = obj.video.name.replace("wiki/articles/video/", "")
                    prev_attach_dict = {
                       "video_id": obj.id,
                       "file_name":  file_name,
                       "error": f"Видео {file_name} уже привязано к другой статье"
                    }
                    errors.append(prev_attach_dict)

        for id in missing_images:
            img_dct = {
                "image_id": id,
                "error": f"Изображение c id={id} остутствует."
            }
            errors.append(img_dct)

        for id in missing_videos:
            video_dct = {
                "video_id": id,
                "error": f"Видео c id={id} остутствует."
            }
            errors.append(video_dct)

        # Передаем информацию об отсутствующих медиафайлах в контекст сериализатора
        self.context['errors'] = errors

        return article