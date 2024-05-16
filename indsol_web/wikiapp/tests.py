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

    # CREATE METHOD READ
    def test_wiki_create(self):
        body = {"name": "test2"}
        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wiki.objects.count(), 1)
        self.assertEqual(Wiki.objects.get().name, "test2")
