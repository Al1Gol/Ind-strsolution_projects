from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import json
from PIL import Image

from authapp.models import Users


# Тестирование списка пользователей
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
        self.user_url = "/api/v1/auth/users/"

    #######################################################################
    ########################## TEST CREATE USERS ##########################
    #######################################################################

    def test_users(self):
        body = {
            "username": "test_user_1",
            "password": "test_password",
        }

        # Создание записи в Users
        post_response = self.client.post(self.user_url, body, format="json")
        user_id_1 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        body = {
            "username": "test_user_2",
            "password": "test_password",
        }
        post_response = self.client.post(self.user_url, body, format="json")
        user_id_2 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        #######################################################################
        ########################## TEST READ USERS #############################
        #######################################################################

        # Получаем список экземпляров Wiki
        get_response = self.client.get(self.user_url, {}, format="json")

        # Проверям получение
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Users.objects.get(id=user_id_1).username, "test_user_1")
        self.assertEqual(Users.objects.count(), 3)

        # Необходимо дописать Users для данного теста
        """
        body = {
            "username": "test_user_1",
            "password": "test_password",
            "email": "mail@mail.ru",
            "inn": 123455678,
            "kpp": 355521222,
        }
        post_response = self.client.post(self.user_url, body, format="json")
        user_id_2 = json.loads(post_response.content)["id"]
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # Получаем список экземпляров Wiki
        get_response = self.client.get(self.user_url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Users.objects.get(id=user_id_2).username, "test_user_1")
        self.assertEqual(Users.objects.count(), 3)
        """
        #######################################################################
        ########################## TEST UPDATE USERS ###########################
        #######################################################################

        # Производим полное (PUT) обнвление экземпляра Users
        body = {
            "username": "user_upd_put",
            "password": "123",
        }
        put_response = self.client.put(
            self.user_url + f"{user_id_2}/", body, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(self.user_url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Users.objects.count(), 3)
        self.assertEqual(Users.objects.get(id=user_id_2).username, "user_upd_put")

        # Производим частичное обнвление экземпляра Users
        body = {
            "username": "user_upd_patch",
        }
        patch_response = self.client.patch(
            self.user_url + f"{user_id_2}/", body, format="json"
        )

        # Производмм проверку результата
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Users.objects.count(), 3)
        self.assertEqual(Users.objects.get(id=user_id_2).username, "user_upd_patch")

        # Проверка редактирования не существующего экземпляра Users
        patch_response = self.client.patch(
            self.user_url + f"{user_id_2+1}/", body, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        #######################################################################
        ########################## TEST DELETE USERS ###########################
        #######################################################################

        # Проверка удаления экземпляра Wiki
        delete_response = self.client.delete(
            self.user_url + f"{user_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Users.objects.count(), 2)

        # Проверка удаление не существующего экземпляра Wiki
        delete_response = self.client.delete(
            self.user_url + f"{user_id_2}/", {}, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Users.objects.count(), 2)
