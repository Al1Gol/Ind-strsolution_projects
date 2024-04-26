from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet, mixins
from indsol_web.permissions import ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly
from indsol_web.exceptions import MediaValidationError

from newsapp.models import News, Media
from newsapp.serializers import NewsSerializer, MediaSerializer
from newsapp.filters import MediaFilter, NewsDateFilter


# Create your views here.
class NewsViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by("created_at")
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]
    search_fields = ["created_at", "title"]
    filter_backends = [filters.SearchFilter]
    filterset_class = NewsDateFilter

    def perform_create(self, serializer):
        serializer.save()


class MediaViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
    permission_classes = [ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly]
    filterset_class = MediaFilter

    # Валидация по количеству media перед сохранением
    def perform_create(self, serilizer):
        media_filter = Media.objects.filter(news_id=self.request.data["news_id"])
        if len(media_filter) < 10:
            serilizer.save()
        else:
            raise MediaValidationError()
