from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render
from authapp.models import Wiki_Permissions, Users
from wikiapp.filters import MenuFilter, ArticlesFilter, FilesFilter, SectionsFilter
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
from indsol_web.exceptions import ForbiddenError
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from django.shortcuts import get_object_or_404
from indsol_web.permissions import ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly, PublicReadAndOnlyOwnerOrAdminUpdate
from indsol_web.permissions import (
    WikiPermission,
    MenuWikiPermission,
    SectionsWikiPermission,
    ArticlesWikiPermission,
    FilesWikiPermission,
    ImagesWikiPermission,
    VideoWikiPermission,
)

# LOG = logging.getLogger('django.request')


class WikiViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    '''
    Список баз знаний
    '''
    serializer_class = WikiSerializer
    queryset = Wiki.objects.all().order_by("created_at")
    permission_classes = [WikiPermission]

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
           queryset = Wiki.objects.none()
           
        else:
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            queryset = Wiki.objects.filter(id__in=perm_ids).order_by("created_at")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        obj_id = self.kwargs.get('pk')
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = obj_id).filter(read = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        

    def perform_create(self, serializer):
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.is_superuser is None:
            raise ForbiddenError()
        else:
            serializer.save()

    def perform_update(self, serializer):
        obj_id = self.kwargs.get('pk')
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = obj_id).filter(update = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            serializer.save()

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.is_superuser == False:
            raise ForbiddenError()
        else:
            instance.delete()
            
    


class MenuViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    '''
    Список меню в БЗ
    '''
    serializer_class = MenuSerializer
    queryset = Menu.objects.all().order_by("order")
    permission_classes = [MenuWikiPermission]
    filterset_class = MenuFilter
    """
    def list(self, request, *args, **kwargs):
        queryset = Menu.objects.all().order_by("created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    """

    
    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
           queryset = Menu.objects.none()
        else:
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            queryset = Menu.objects.filter(wiki_id_id__in=perm_ids).order_by("created_at")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        obj_id = self.kwargs.get('pk')
        menu = Menu.objects.get(id=obj_id)
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = menu.wiki_id_id).filter(read = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance = self.get_object()
            serializer = self.get_serializer(menu)
            return Response(serializer.data)


    def perform_create(self, serializer):
        obj_id = serializer.validated_data.get('wiki_id')
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = obj_id).filter(create = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            serializer.save()


    def perform_update(self, serializer):
        obj_id = self.kwargs.get('pk')
        menu = Menu.objects.get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = menu.wiki_id_id).filter(update = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            # Проверяем не входит ли получаемый id в список недоступных
            wiki_id = serializer.validated_data.get('wiki_id')
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(update = True).values_list('wiki_id', flat=True)
            
            if wiki_id.id not in perm_ids:
                raise ForbiddenError("Вики, указанная при обновлении, недоступна данному пользователю.")
            serializer.save()

    def perform_destroy(self, instance):
        obj_id = self.kwargs.get('pk')
        menu = Menu.objects.get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
                raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = menu.wiki_id_id).filter(delete = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance.delete()


class SectionsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    '''
    Список разделов в БЗ
    '''
    serializer_class = SectionsSerializer
    queryset = Sections.objects.all().order_by("order")
    permission_classes = [SectionsWikiPermission]
    filterset_class = SectionsFilter

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
           queryset = Menu.objects.none()
        else:
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            menu_ids = Menu.objects.filter(wiki_id_id__in=perm_ids).values_list('id', flat=True)
            queryset = Sections.objects.filter(menu_id_id__in=menu_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        obj_id = self.kwargs.get('pk')
        wiki = Sections.objects.select_related('menu_id__wiki_id').get(id=obj_id)
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.menu_id.wiki_id).filter(read = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        

    def perform_create(self, serializer):
        parent = Menu.objects.get(id=self.request.data["menu_id"])
        if parent.is_article == True:
            raise ValidationError(
                "Данный родитель уже используется для хранения статьи"
            )
        menu = serializer.validated_data.get('menu_id')
        wiki_id = Menu.objects.get(id=menu.id).wiki_id
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki_id).filter(create = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            serializer.save()


    def perform_update(self, serializer):
        obj_id = self.kwargs.get('pk')
        wiki = Sections.objects.select_related('menu_id__wiki_id').get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)

       
        if user.wiki_group is None:
            raise ForbiddenError()
        
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.menu_id.wiki_id).filter(update = True)
        if len(perm)==0:
            raise ForbiddenError()    
        else:
            # Проверяем не входит ли получаемый id в список недоступных
            menu = serializer.validated_data.get('menu_id')
            wiki_id = Menu.objects.get(id=menu.id).wiki_id.id
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(update = True).values_list('wiki_id', flat=True)
            
            if wiki_id not in perm_ids:
                raise ForbiddenError("Пункт меню, указанный при обновлении, недоступен данному пользователю.")
            
            serializer.save()

    def perform_destroy(self, instance):
        obj_id = self.kwargs.get('pk')
        wiki = Sections.objects.select_related('menu_id__wiki_id').get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
                raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.menu_id.wiki_id).filter(delete = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance.delete()

    # Не отрабатывает корректно, так как при удалении не существующей записи вместо 404 Not Found выдает 502 You can't delete object with includes
    """
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return JsonResponse(
                {"error": "You can't delete object with includes"}, status=502
            )
    """


class ArticleViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    '''
    Список статей в БЗ
    '''
    serializer_class = ArticlesSerializer
    queryset = Articles.objects.all().order_by("order")
    permission_classes = [ArticlesWikiPermission]
    filterset_class = ArticlesFilter


    #Сделал только для статей в разделах. Если делать статьи в меню - нажо доработать
    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
           queryset = Menu.objects.none()
        else:
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            menu_ids = Menu.objects.filter(wiki_id_id__in=perm_ids).values_list('id', flat=True)
            section_ids = Sections.objects.filter(menu_id_id__in=menu_ids).values_list('id', flat=True)
            queryset = Articles.objects.filter(section_id_id__in=section_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    #Сделал только для статей в разделах. Если делать статьи в меню - нажо доработать
    def retrieve(self, request, *args, **kwargs):
        obj_id = self.kwargs.get('pk')
        wiki = Articles.objects.select_related('section_id__menu_id__wiki_id').get(id=obj_id)
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.section_id.menu_id.wiki_id).filter(read = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)


    # Валидация количества родителей и выставление отметки is_article для родителя
    def perform_create(self, serializer):
        section = serializer.validated_data.get('section_id')
        wiki_id = Menu.objects.get(id=section.menu_id.id).wiki_id
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki_id).filter(create = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
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


    def perform_update(self, serializer):
        obj_id = self.kwargs.get('pk')
        wiki = Articles.objects.select_related('section_id__menu_id__wiki_id').get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)

        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.section_id.menu_id.wiki_id).filter(update = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            # Проверяем не входит ли получаемый id в список недоступных
            section = serializer.validated_data.get('section_id')
            wiki_id = Menu.objects.get(id=section.menu_id.id).wiki_id.id

            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            if wiki_id not in perm_ids:
                raise ForbiddenError("Раздел, указанный при обновлении, недоступна данному пользователю.")
            serializer.save()


    # Необходимо дописать снятие галочки is_article при удалении статьи
    def perform_destroy(self, instance):
        obj_id = self.kwargs.get('pk')
        wiki = Articles.objects.select_related('section_id__menu_id__wiki_id').get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
                raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.section_id.menu_id.wiki_id).filter(delete = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
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
    '''
    Список файлов прикрепленных к статьям в БЗ
    '''
    serializer_class = FilesSerializer
    queryset = Files.objects.all().order_by("created_at")
    filterset_class = FilesFilter
    permission_classes = [FilesWikiPermission]


    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
           queryset = Menu.objects.none()
        else:
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            menu_ids = Menu.objects.filter(wiki_id_id__in=perm_ids).values_list('id', flat=True)
            section_ids = Sections.objects.filter(menu_id_id__in=menu_ids).values_list('id', flat=True)
            article_ids = Articles.objects.filter(section_id_id__in=section_ids).values_list('id', flat=True)
            queryset = Files.objects.filter(article_id_id__in=article_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        obj_id = self.kwargs.get('pk')
        wiki = Files.objects.select_related('article_id__section_id__menu_id__wiki_id').get(id=obj_id)
        user_id = request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.article_id.section_id.menu_id.wiki_id).filter(read = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        

    def perform_create(self, serializer):
        article = serializer.validated_data.get('article_id')
        wiki_id = Menu.objects.get(id=article.section_id.menu_id.id).wiki_id
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki_id).filter(create = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            serializer.save()

    #Надо запретить менять id на запрещенный
    def perform_update(self, serializer):
        obj_id = self.kwargs.get('pk')
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)

        wiki = Files.objects.select_related('article_id__section_id__menu_id__wiki_id').get(id=obj_id)
        if user.wiki_group is None:
            raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.article_id.section_id.menu_id.wiki_id).filter(update = True)
        
        if len(perm)==0:
            raise ForbiddenError()
        else:
             # Проверяем не входит ли получаемый id в список недоступных
            article = serializer.validated_data.get('article_id')
            wiki_id = Menu.objects.get(id=article.section_id.menu_id.id).wiki_id.id
            perm_ids = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(read = True).values_list('wiki_id', flat=True)
            if wiki_id not in perm_ids:
                raise ForbiddenError("Статья, указанная при обновлении, недоступна данному пользователю.")
            serializer.save()


    def perform_destroy(self, instance):
        obj_id = self.kwargs.get('pk')
        wiki = Files.objects.select_related('article_id__section_id__menu_id__wiki_id').get(id=obj_id)
        user_id = self.request.user.id
        user = Users.objects.get(id=user_id)
        if user.wiki_group is None:
                raise ForbiddenError()
        perm = Wiki_Permissions.objects.filter(wiki_group = user.wiki_group).filter(wiki_id = wiki.article_id.section_id.menu_id.wiki_id).filter(delete = True)
        if len(perm)==0:
            raise ForbiddenError()
        else:
            instance.delete()


class ImagesViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    '''
    Список изображений прикрепленных к статьям в БЗ
    '''
    serializer_class = ImagesSerializer
    queryset = Images.objects.all()
    permission_classes = [ImagesWikiPermission]


class VideosViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    '''
    Список видео прикрепленных к статьям в БЗ
    '''
    serializer_class = VideosSerializer
    queryset = Videos.objects.all()
    permission_classes = [VideoWikiPermission]
