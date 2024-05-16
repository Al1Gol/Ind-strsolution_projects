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
        body = {"name": "test2"}
        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(Wiki.objects.get().name, "test2")

    # READ METHOD TEST WIKI
    def test_wiki_read(self):
        # Создаем первую запись
        body = {
            "name": "test_1",
        }
        post_response = self.client.post(self.url, body, format="json")
        id_1 = json.loads(post_response.content)["id"]

        # Получаем список новостей
        get_response = self.client.get(self.url, {}, format="json")

        # Проверям полученную новость
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.get(id=id_1).name, "test_1")
        self.assertEqual(Wiki.objects.count(), 1)

        # Создаем вторую запись
        body = {
            "name": "test_2",
        }
        post_response = self.client.post(self.url, body, format="json")
        id_2 = json.loads(post_response.content)["id"]

        # Получаем список новостей
        get_response = self.client.get(self.url, {}, format="json")

        # Проверям обе полученные новости
        self.assertEqual(Wiki.objects.count(), 2)
        self.assertEqual(Wiki.objects.get(id=id_1).name, "test_1")
        self.assertEqual(Wiki.objects.get(id=id_2).name, "test_2")

    # UPDATE METHOD TEST WIKI
    def test_wiki_update(self):

        # Создаем запись
        body = {
            "name": "test original",
        }
        post_response = self.client.post(self.url, body, format="json")
        id = json.loads(post_response.content)["id"]
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(Wiki.objects.get(id=id).name, "test original")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # Производим полное (PUT) обнвление
        body = {
            "name": "test edited",
        }
        put_response = self.client.put(self.url + f"{id}/", body, format="json")
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.get(id=id).name, "test edited")

        # Производим частичное обнвление
        body = {
            "name": "edited patch",
        }
        patch_response = self.client.patch(self.url + f"{id}/", body, format="json")

        # Получаем отредактированное значение
        get_response = self.client.get(self.url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wiki.objects.get(id=id).name, "edited patch")

        # Проверка редактирования не существующей новости
        patch_response = self.client.patch(self.url + f"{id+1}/", body, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

    # DELETE METHOD WIKI
    def test_wiki_delete(self):

        # Создаем запись
        body = {
            "name": "test delete",
        }
        post_response = self.client.post(self.url, body, format="json")
        id = json.loads(post_response.content)["id"]
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # Проверка удаления записи
        delete_response = self.client.delete(self.url + f"{id}/", {}, format="json")
        self.assertEqual(Wiki.objects.count(), 0)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка удаление не существующей записи
        delete_response = self.client.delete(self.url + f"{id}/", {}, format="json")
        self.assertEqual(Wiki.objects.count(), 0)
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
