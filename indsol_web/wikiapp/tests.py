from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import json
from PIL import Image

from authapp.models import Users
from wikiapp.models import Wiki, Menu, Sections


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
        self.section_url = "/api/v1/wiki/sections/"

    #######################################################################
    ########################## TEST CREATE WIKI ###########################
    #######################################################################

    def test_wiki_create(self):
        wiki_body = {
            "name": "wiki_test_create_1",
        }

        # Создание записи в Wiki
        post_response = self.client.post(self.wiki_url, wiki_body, format="json")
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
        wiki_body_2 = {
            "name": "wiki_test_create_2",
        }
        post_response = self.client.post(self.wiki_url, wiki_body_2, format="json")
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

        menu_body = {
            "wiki_id": wiki_id_1,
            "name": "menu_test_create_1",
        }
        # Создание записи в Menu
        post_response = self.client.post(self.menu_url, menu_body, format="json")
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
        menu_body_2 = {
            "wiki_id": wiki_id_1,
            "name": "menu_test_create_2",
        }
        post_response = self.client.post(self.menu_url, menu_body_2, format="json")
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
            self.menu_url + f"{menu_id_1}/", body, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.menu_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(Menu.objects.get(id=menu_id_1).name, "menu_test_update_put")

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
        post_response = self.client.post(self.section_url, body, format="json")
        section_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sections.objects.count(), 1)
        self.assertEqual(Sections.objects.get().name, "section_test_create_1")

        # Получаем список экземпляров Sections
        get_response = self.client.get(self.section_url, {}, format="json")

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
        post_response = self.client.post(self.section_url, body, format="json")
        section_id_2 = json.loads(post_response.content)["id"]
