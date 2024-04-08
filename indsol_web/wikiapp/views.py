from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render
from wikiapp.filters import ArticlesFilter, FilesFilter, SectionsFilter
from wikiapp.models import Wiki, Articles, Files, Images, Menu, Sections, Videos
from wikiapp.serializers import (
    WikiSerializer,
    ArticlesSerializer,
    FilesSerializer,
    ImagesSerializer,
    MenuSerializer,
    SectionsSerializer,
    VideosSerializer,
)
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from indsol_web.permissions import ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly

# LOG = logging.getLogger('django.request')


class WikiViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = WikiSerializer
    queryset = Wiki.objects.all().order_by("created_at")
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Menu.objects.all().order_by("created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()


class MenuViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all().order_by("created_at")
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Menu.objects.all().order_by("created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()


class SectionsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = SectionsSerializer
    queryset = Sections.objects.all().order_by("created_at")
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]
    filterset_class = SectionsFilter

    def perform_create(self, serializer):
        parent = Menu.objects.get(id=self.request.data["menu_id"])
        if parent.is_article == True:
            raise ValidationError(
                "Данный родитель уже используется для хранения статьи"
            )
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return JsonResponse(
                {"error": "You can't delete object with includes"}, status=502
            )


class ArticleViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ArticlesSerializer
    queryset = Articles.objects.all().order_by("created_at")
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]
    filterset_class = ArticlesFilter

    # Валидация количества родителей и выставление отметки is_article для родителя
    def perform_create(self, serializer):
        count_parent = 0
        if self.request.POST.get("menu_id") or self.request.data.get("menu_id"):
            count_parent += 1
            parent = Menu.objects.get(id=self.request.data["menu_id"])
            parent.is_article = True
        if self.request.POST.get("section_id") or self.request.data.get("section_id"):
            count_parent += 1
            parent = Sections.objects.get(id=self.request.data["section_id"])
            parent.is_article = True
        if (count_parent > 1) or (count_parent == 0):
            raise ValidationError(
                f"Статья может иметь привязку к одному родительскому элементу. Текущее количество родительских элементов - {count_parent}"
            )
        parent.save()
        serializer.save()

    # Необходимо дописать снятие галочки is_article при удалении статьи
    def perform_destroy(self, instance):
        if instance.menu_id:
            parent = Menu.objects.get(id=instance.menu_id.id)
            parent.is_article = False
        elif instance.section_id:
            parent = Sections.objects.get(id=instance.section_id.id)
            parent.is_article = False
        parent.save()
        instance.delete()


class FilesViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = FilesSerializer
    queryset = Files.objects.all().order_by("created_at")
    filterset_class = FilesFilter
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]


class ImagesViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ImagesSerializer
    queryset = Images.objects.all()
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]


class VideosViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = VideosSerializer
    queryset = Videos.objects.all()
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]
