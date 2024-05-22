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

        # Получаем список экземпляров Wiki
        get_response = self.client.get(self.user_url, {}, format="json")

        # Проверям полученнку
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Users.objects.get(id=user_id_1).username, "test_user_1")
        self.assertEqual(Users.objects.count(), 2)
