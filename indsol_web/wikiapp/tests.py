from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import json
from PIL import Image

from authapp.models import Users
from wikiapp.models import Wiki


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
        self.url = "/api/v1/wiki/list/"

    # CREATE METHOD TEST WIKI
    def test_wiki_create(self):
        wiki_body = {"name": "test_1"}

        # Создание записи в Wiki
        post_response = self.client.post(self.url, wiki_body, format="json")
        wiki_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(Wiki.objects.get().name, "test_1")

        # Получаем список экземпляров WIKI
        get_response = self.client.get(self.url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.get(id=wiki_id_1).name, "test_1")
        self.assertEqual(Wiki.objects.count(), 1)

        # Создание второг экземпляра WIKI
        wiki_body_2 = {
            "name": "test_2",
        }
        post_response = self.client.post(self.url, wiki_body_2, format="json")
        wiki_id_2 = json.loads(post_response.content)["id"]

        # Получаем список wiki
        get_response = self.client.get(self.url, {}, format="json")

        # Проверям оба полученных экземпляра WIKI
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=wiki_id_1).name, "test_1")
        self.assertEqual(Wiki.objects.get(id=wiki_id_2).name, "test_2")

        # Производим полное (PUT) обнвление экземпляра WIKI
        body = {
            "name": "test edited",
        }
        put_response = self.client.put(self.url + f"{wiki_id_2}/", body, format="json")
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=wiki_id_2).name, "test edited")

        # Производим частичное обнвление экземпляра WIKI
        body = {
            "name": "edited patch",
        }
        patch_response = self.client.patch(
            self.url + f"{wiki_id_2}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=wiki_id_2).name, "edited patch")

        # Проверка редактирования не существующего экземпляра WIKI
        patch_response = self.client.patch(
            self.url + f"{wiki_id_2+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверка удаления экземпляра WIKI
        delete_response = self.client.delete(
            self.url + f"{wiki_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wiki.objects.count(), 1)

        # Проверка удаление не существующего экземпляра WIKI
        delete_response = self.client.delete(
            self.url + f"{wiki_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Wiki.objects.count(), 1)
