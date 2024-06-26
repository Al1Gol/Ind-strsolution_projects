from django.test import TestCase
import datetime
import pytz
from unittest import mock

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import json
from PIL import Image
from io import BytesIO

from authapp.models import Users
from wikiapp.models import Wiki, Menu, Sections, Articles, Files


# Тестирование списка меню
class APIWikiTests(APITestCase):
    def setUp(self):
        # Получаем JWT токен для пользователя admin
        # Передаем его в заголвок
        user = Users.objects.create_user(
            username="test_admin", password="test_admin", is_staff=True
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.wiki_url = "/api/v1/wiki/list/"
        self.menu_url = "/api/v1/wiki/menu/"
        self.sections_url = "/api/v1/wiki/sections/"
        self.articles_url = "/api/v1/wiki/articles/"
        self.files_url = "/api/v1/wiki/files/"

    # Создание файла
    def create_valid_image(self):
        image_file = BytesIO()
        image = Image.new("RGBA", size=(50, 50), color=(155, 0, 0))
        image.save(image_file, "png")
        image_file.name = "test_image.jpg"
        image_file.seek(0)
        return image_file

    #######################################################################
    ########################## TEST CREATE WIKI ###########################
    #######################################################################

    def test_wiki(self):
        body = {
            "name": "wiki_test_create_1",
        }

        # Создание записи в Wiki
        post_response = self.client.post(self.wiki_url, body, format="json")
        wiki_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(Wiki.objects.get().name, "wiki_test_create_1")

        # Получаем список экземпляров Wiki
        get_response = self.client.get(self.wiki_url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.get(id=wiki_id_1).name, "wiki_test_create_1")
        self.assertEqual(Wiki.objects.count(), 1)

        # Создание второг экземпляра Wiki
        body = {
            "name": "wiki_test_create_2",
        }
        post_response = self.client.post(self.wiki_url, body, format="json")
        wiki_id_2 = json.loads(post_response.content)["id"]

        #######################################################################
        ########################## TEST READ WIKI #############################
        #######################################################################

        # Получаем список wiki
        get_response = self.client.get(self.wiki_url, {}, format="json")

        # Проверям оба полученных экземпляра WIKI
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=wiki_id_1).name, "wiki_test_create_1")
        self.assertEqual(Wiki.objects.get(id=wiki_id_2).name, "wiki_test_create_2")

        #######################################################################
        ########################## TEST UPDATE WIKI ###########################
        #######################################################################

        # Производим полное (PUT) обнвление экземпляра Wiki
        body = {
            "name": "wiki_test_update_put",
        }
        put_response = self.client.put(
            self.wiki_url + f"{wiki_id_2}/", body, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.wiki_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=wiki_id_2).name, "wiki_test_update_put")

        # Производим частичное обнвление экземпляра Wiki
        body = {
            "name": "wiki_test_update_patch",
        }
        patch_response = self.client.patch(
            self.wiki_url + f"{wiki_id_2}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=wiki_id_2).name, "wiki_test_update_patch")

        # Проверка редактирования не существующего экземпляра Wiki
        patch_response = self.client.patch(
            self.wiki_url + f"{wiki_id_2+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        #######################################################################
        ########################## TEST DELETE WIKI ###########################
        #######################################################################

        # Проверка удаления экземпляра Wiki
        delete_response = self.client.delete(
            self.wiki_url + f"{wiki_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wiki.objects.count(), 1)

        # Проверка удаление не существующего экземпляра Wiki
        delete_response = self.client.delete(
            self.wiki_url + f"{wiki_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Wiki.objects.count(), 1)

        #######################################################################
        ########################## TEST CREATE MENU ###########################
        #######################################################################

        body = {
            "wiki_id": wiki_id_1,
            "name": "menu_test_create_1",
        }
        # Создание записи в Menu
        post_response = self.client.post(self.menu_url, body, format="json")
        menu_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().name, "menu_test_create_1")

        # Получаем список экземпляров Menu
        get_response = self.client.get(self.menu_url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Menu.objects.get(id=menu_id_1).name, "menu_test_create_1")
        self.assertEqual(Menu.objects.count(), 1)

        # Создание второг экземпляра Menu
        body = {
            "wiki_id": wiki_id_1,
            "name": "menu_test_create_2",
        }
        post_response = self.client.post(self.menu_url, body, format="json")
        menu_id_2 = json.loads(post_response.content)["id"]

        #######################################################################
        ########################## TEST READ MENU #############################
        #######################################################################

        # Получаем список Menu
        get_response = self.client.get(self.menu_url, {}, format="json")

        # Проверям оба полученных экземпляра Menu
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(Menu.objects.get(id=menu_id_1).name, "menu_test_create_1")
        self.assertEqual(Menu.objects.get(id=menu_id_2).name, "menu_test_create_2")

        #######################################################################
        ########################## TEST UPDATE MENU ###########################
        #######################################################################

        body = {
            "wiki_id": wiki_id_1,
            "name": "menu_test_update_put",
            "file": "",
        }
        put_response = self.client.put(
            self.menu_url + f"{menu_id_2}/", body, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.menu_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(Menu.objects.get(id=menu_id_2).name, "menu_test_update_put")

        # Производим частичное обнвление экземпляра Menu
        body = {
            "name": "menu_test_update_patch",
        }
        patch_response = self.client.patch(
            self.menu_url + f"{menu_id_2}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(Menu.objects.get(id=menu_id_2).name, "menu_test_update_patch")

        # Проверка редактирования не существующего экземпляра Menu
        patch_response = self.client.patch(
            self.menu_url + f"{menu_id_2+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        #######################################################################
        ########################## TEST DELETE MENU ###########################
        #######################################################################

        # Проверка удаления экземпляра Menu
        delete_response = self.client.delete(
            self.menu_url + f"{menu_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 1)

        # Проверка удаление не существующего экземпляра Menu
        delete_response = self.client.delete(
            self.menu_url + f"{menu_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Menu.objects.count(), 1)

        #######################################################################
        ######################## TEST CREATE SECTIONS #########################
        #######################################################################

        body = {
            "menu_id": menu_id_1,
            "name": "section_test_create_1",
        }

        # Создание записи в Sections
        post_response = self.client.post(self.sections_url, body, format="json")
        section_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sections.objects.count(), 1)
        self.assertEqual(Sections.objects.get().name, "section_test_create_1")

        # Получаем список экземпляров Sections
        get_response = self.client.get(self.sections_url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Sections.objects.get(id=section_id_1).name, "section_test_create_1"
        )
        self.assertEqual(Sections.objects.count(), 1)

        # Создание второг экземпляра Sections
        body = {
            "menu_id": menu_id_1,
            "name": "section_test_create_2",
        }
        post_response = self.client.post(self.sections_url, body, format="json")
        section_id_2 = json.loads(post_response.content)["id"]

        #######################################################################
        ########################## TEST READ SECTIONS #############################
        #######################################################################

        # Получаем список Sections
        get_response = self.client.get(self.sections_url, {}, format="json")

        # Проверям оба полученных экземпляра Sections
        self.assertEqual(Sections.objects.count(), 2)
        self.assertEqual(
            Sections.objects.get(id=section_id_1).name, "section_test_create_1"
        )
        self.assertEqual(
            Sections.objects.get(id=section_id_2).name, "section_test_create_2"
        )

        #######################################################################
        ########################## TEST UPDATE SECTIONS ###########################
        #######################################################################

        body = {
            "menu_id": menu_id_1,
            "name": "section_test_update_put",
            "file": "",
        }
        put_response = self.client.put(
            self.sections_url + f"{section_id_2}/", body, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.sections_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sections.objects.count(), 2)
        self.assertEqual(
            Sections.objects.get(id=menu_id_2).name, "section_test_update_put"
        )

        # Производим частичное обнвление экземпляра Sections
        body = {
            "name": "section_test_update_patch",
        }
        patch_response = self.client.patch(
            self.sections_url + f"{section_id_2}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sections.objects.count(), 2)
        self.assertEqual(
            Sections.objects.get(id=section_id_2).name, "section_test_update_patch"
        )

        # Проверка редактирования не существующего экземпляра Sections
        patch_response = self.client.patch(
            self.sections_url + f"{section_id_2+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        #######################################################################
        ######################## TEST DELETE SECTIONS #########################
        #######################################################################

        # Проверка удаления экземпляра Sections
        delete_response = self.client.delete(
            self.sections_url + f"{section_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sections.objects.count(), 1)

        # Проверка удаление не существующего экземпляра Sections
        delete_response = self.client.delete(
            self.sections_url + f"{section_id_2+1}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Sections.objects.count(), 1)

        #######################################################################
        ######################## TEST CREATE ARTICLES #########################
        #######################################################################

        body = {
            "section_id": section_id_1,
            "name": "article_test_create_title_1",
            "text": "article_test_create_text_1",
        }

        # Создание записи в Articles
        post_response = self.client.post(self.articles_url, body, format="json")
        articles_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Articles.objects.count(), 1)
        self.assertEqual(Articles.objects.get().name, "article_test_create_title_1")
        self.assertEqual(Articles.objects.get().text, "article_test_create_text_1")

        # Получаем список экземпляров Articles
        get_response = self.client.get(self.articles_url, {}, format="json")

        # Проверям статус
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Articles.objects.count(), 1)

        # Создание второг экземпляра Articles
        body = {
            "section_id": section_id_1,
            "name": "article_test_create_title_2",
            "text": "article_test_create_text_2",
        }
        post_response = self.client.post(self.articles_url, body, format="json")
        articles_id_2 = json.loads(post_response.content)["id"]

        #######################################################################
        ########################## TEST READ ARTICLES #########################
        #######################################################################

        # Получаем список Articles
        get_response = self.client.get(self.articles_url, {}, format="json")

        # Проверям оба полученных экземпляра Articles
        self.assertEqual(Articles.objects.count(), 2)
        self.assertEqual(
            Articles.objects.get(id=articles_id_1).name, "article_test_create_title_1"
        )
        self.assertEqual(
            Articles.objects.get(id=articles_id_1).text, "article_test_create_text_1"
        )
        self.assertEqual(
            Articles.objects.get(id=articles_id_2).name, "article_test_create_title_2"
        )
        self.assertEqual(
            Articles.objects.get(id=articles_id_2).text, "article_test_create_text_2"
        )

        #######################################################################
        ########################## TEST UPDATE ARTICLES ###########################
        #######################################################################

        body = {
            "menu_id": section_id_1,
            "name": "articles_test_update_put_title",
            "text": "articles_test_update_put_text",
        }
        put_response = self.client.put(
            self.articles_url + f"{articles_id_2}/", body, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.articles_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Articles.objects.count(), 2)
        self.assertEqual(
            Articles.objects.get(id=articles_id_2).name,
            "articles_test_update_put_title",
        )
        self.assertEqual(
            Articles.objects.get(id=articles_id_2).text, "articles_test_update_put_text"
        )

        # Производим частичное обнвление экземпляра Articles
        body = {
            "name": "articles_test_update_patch_title",
        }
        patch_response = self.client.patch(
            self.articles_url + f"{articles_id_2}/", body, format="json"
        )
        body = {
            "text": "articles_test_update_patch_text",
        }
        patch_response = self.client.patch(
            self.articles_url + f"{articles_id_2}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Articles.objects.count(), 2)
        self.assertEqual(
            Articles.objects.get(id=section_id_2).name,
            "articles_test_update_patch_title",
        )
        self.assertEqual(
            Articles.objects.get(id=section_id_2).text,
            "articles_test_update_patch_text",
        )

        # Проверка редактирования не существующего экземпляра Articles
        patch_response = self.client.patch(
            self.sections_url + f"{section_id_2+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        #######################################################################
        ######################## TEST DELETE ARTICLES #########################
        #######################################################################

        # Проверка удаления экземпляра Articles
        delete_response = self.client.delete(
            self.articles_url + f"{articles_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Articles.objects.count(), 1)

        # Проверка удаление не существующего экземпляра Articles
        delete_response = self.client.delete(
            self.articles_url + f"{articles_id_2+1}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Articles.objects.count(), 1)

        #######################################################################
        ########################## TEST CREATE FILES ###########################
        #######################################################################
        file = self.create_valid_image()
        body = {
            "article_id": articles_id_1,
            "name": "test name",
            "file": file,
        }

        # Создание записи в Files
        post_response = self.client.post(self.files_url, body, format="multipart")
        files_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Files.objects.count(), 1)

        # Получаем список экземпляров Files
        get_response = self.client.get(self.files_url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Files.objects.count(), 1)

        #######################################################################
        ########################## TEST READ FILES #########################
        #######################################################################

        # Получаем список Files
        get_response = self.client.get(self.files_url, {}, format="json")

        # Проверям оба полученных экземпляра Files
        self.assertEqual(Files.objects.count(), 1)
        self.assertEqual(Files.objects.get(id=files_id_1).name, "test name")

        #######################################################################
        ########################## TEST UPDATE FILSE ###########################
        #######################################################################

        """ Не работает полное обновление по причине остуттсвия обработки auto_now_add и auto_add
        mocked = datetime.datetime(2018, 4, 4, 0, 0, 0, tzinfo=pytz.utc)
        body = {
            "articles_id": articles_id_2,
            "name": "files_test_update_patch_name",
            "file": file,
        }
        put_response = self.client.put(
            self.files_url + f"{files_id_1}/", body, format="multipart"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.articles_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Files.objects.count(), 2)
        self.assertEqual(
            Files.objects.get(id=files_id_1).name,
            "files_test_update_patch_name",
        )
        """
        # Производим частичное обнвление экземпляра Articles
        body = {
            "name": "files_test_update_patch_name",
        }
        patch_response = self.client.patch(
            self.files_url + f"{files_id_1}/", body, format="json"
        )

        # Производим частичное обнвление экземпляра Articles
        body = {
            "name": "files_test_update_patch_name",
        }
        patch_response = self.client.patch(
            self.files_url + f"{files_id_1}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Files.objects.count(), 1)
        self.assertEqual(
            Files.objects.get(id=files_id_1).name,
            "files_test_update_patch_name",
        )

        # Проверка редактирования не существующего экземпляра Articles
        patch_response = self.client.patch(
            self.files_url + f"{files_id_1+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)
