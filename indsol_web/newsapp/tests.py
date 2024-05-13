from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http.response import JsonResponse
import json

from authapp.models import Users
from newsapp.models import News
from .views import NewsViewSet


class APINewsTests(APITestCase):
    def setUp(self):
        # Получаем JWT токен для пользователя admin
        # Передаем его в заголвок
        user = Users.objects.create_user(
            username="test_admin", password="test_admin", is_staff=True
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    # Тест корректного создания новости
    def test_news_create(self):
        url = "/api/v1/news/list/"
        body = {
            "title": "test_create_news",
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc non quam volutpat, venenatis nibh nec, tempor nibh. In at tellus imperdiet, \
                finibus quam at, imperdiet quam. Sed massa magna, ultricies sit amet malesuada eu, tempor eget eros. Nulla sit amet elementum elit. Suspendisse ac ultrices diam. \
                Donec fringilla commodo justo in pellentesque. Nullam faucibus erat vel purus gravida, vel porta sem ullamcorper. Donec elit magna, cursus ac leo et, gravida blandit\
                 enim. Cras convallis erat nunc, vel consequat ipsum bibendum non. Nulla ultrices dignissim nisl, nec vestibulum quam interdum quis. Donec lobortis, risus sed maximus\
                 finibus, neque lorem efficitur dui, ut laoreet nunc ante sed nibh.Nullam vulputate neque vel tempus pretium. Nulla facilisi. Phasellus venenatis sem sapien, et vehicula\
                 odio porta nec. Sed sed lacus consequat, bibendum lacus et, congue velit. Proin in libero vel erat egestas lobortis. Cras id sagittis nunc, eget accumsan velit.\
                 Morbi eu pulvinar felis. Integer ut purus pharetra, varius odio ac, efficitur quam. Morbi pharetra nisl id facilisis mattis. Phasellus tincidunt ante non lectus\
                 facilisis porta id id neque. Suspendisse potenti. Maecenas rutrum quam ipsum, nec gravida arcu ullamcorper sit amet. Praesent erat lacus, posuere quis dapibus eu, \
                hendrerit eu felis. Pellentesque varius eros vel condimentum mollis. Mauris maximus at eros quis aliquet. Curabitur malesuada, leo ac auctor convallis, elit sem fermentum \
                tortor, vitae iaculis nisl enim at eros. Cras egestas semper dui, nec varius ligula tempus eu. Fusce vitae erat quis lectus rutrum fermentum vitae at nisi. Aliquam efficitur\
                 quis mauris fermentum pretium. Aliquam lacus purus, tristique faucibus tellus eleifend, euismod consequat ex. Curabitur et porta purus. uspendisse quis luctus lacus, laoreet \
                venenatis lectus. Proin fermentum, est et lacinia molestie, metus nunc sagittis mi, vel dapibus nisl ligula sed elit. Sed malesuada elit at tincidunt mollis. Curabitur ac dui\
                 libero. Mauris nunc eros, ultricies a tristique a, hendrerit sit amet augue. Mauris nibh justo, tempor non nisl et, hendrerit iaculis urna. Donec lectus dolor, elementum eu\
                 dapibus at, condimentum nec velit. Praesent tincidunt orci non venenatis sollicitudin. In accumsan, augue vel gravida fermentum, orci arcu varius turpis, eu elementum ex \
                ipsum eget sapien. Maecenas sed efficitur felis. Proin nunc diam, placerat in varius a, cursus a magna. Nullam efficitur eros sed est sagittis, non venenatis nibh maximus. \
                Curabitur tortor lacus, placerat eget efficitur facilisis, lacinia ut eros.Fusce sed sem sodales, dapibus diam sed, congue orci. Fusce nisl tellus, luctus a ex ut, elementum \
                ultrices enim. Morbi cursus auctor pulvinar. Nullam ac ultricies purus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas elementum\
                 sem vehicula, tempus felis congue, cursus neque. Nam iaculis nisi est, sed feugiat nisl pretium ac. Quisque vel gravida sem. Etiam hendrerit diam eu tristique cursus. Proin ac \
                arcu aliquet, consectetur lacus eu, convallis neque.",
        }
        response = self.client.post(url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.get().title, "test_create_news")
        self.assertEqual(News.objects.get().newsline, False)

    # Тест корректного отображения списка новостей
    def test_news_list(self):
        url = "/api/v1/news/list/"

        # Создаем первую запись
        body = {"title": "test title", "text": "test text"}
        post_response = self.client.post(url, body, format="json")
        id_1 = json.loads(post_response.content)["id"]

        # Получаем список новостей
        get_response = self.client.get(url, {}, format="json")

        # Проверям полученную новость
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content)[0]["title"], "test title")
        self.assertEqual(News.objects.get(id=id_1).title, "test title")
        self.assertEqual(News.objects.get(id=id_1).text, "test text")
        self.assertEqual(News.objects.get(id=id_1).newsline, False)
        self.assertEqual(News.objects.count(), 1)

        # Создаем вторую запись
        body = {"title": "test title 2", "text": "test text 2", "newsline": True}
        post_response = self.client.post(url, body, format="json")
        id_2 = json.loads(post_response.content)["id"]

        # Получаем список новостей
        get_response = self.client.get(url, {}, format="json")

        # Проверям обе полученные новости
        self.assertEqual(News.objects.count(), 2)
        self.assertEqual(News.objects.get(id=id_1).title, "test title")
        self.assertEqual(News.objects.get(id=id_1).text, "test text")
        self.assertEqual(News.objects.get(id=id_1).newsline, False)
        self.assertEqual(News.objects.get(id=id_2).title, "test title 2")
        self.assertEqual(News.objects.get(id=id_2).text, "test text 2")
        self.assertEqual(News.objects.get(id=id_2).newsline, True)

    # Тест корректного обновления новости
    def test_news_update(self):
        url = "/api/v1/news/list/"

        # Создаем запись
        body = {"title": "test title", "text": "test text"}
        post_response = self.client.post(url, body, format="json")
        id = json.loads(post_response.content)["id"]
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # Производим полное (PUT) обнвление
        body = {
            "title": "edited put title",
            "text": "edited put text",
            "newsline": True,
        }
        put_response = self.client.put(url + f"{id}/", body, format="json")
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # Получаем отредактированное значение
        get_response = self.client.get(url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(News.objects.get(id=id).title, "edited put title")
        self.assertEqual(News.objects.get(id=id).text, "edited put text")
        self.assertEqual(News.objects.get(id=id).newsline, True)

        # Производим частичное обнвление
        body = {
            "title": "edited patch title",
        }
        patch_response = self.client.patch(url + f"{id}/", body, format="json")
        body = {
            "text": "edited patch text",
        }
        patch_response = self.client.patch(url + f"{id}/", body, format="json")
        body = {
            "newsline": False,
        }
        patch_response = self.client.patch(url + f"{id}/", body, format="json")

        # Получаем отредактированное значение
        get_response = self.client.get(url, {}, format="json")

        # Производмм проверку результата
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(News.objects.get(id=id).title, "edited patch title")
        self.assertEqual(News.objects.get(id=id).text, "edited patch text")
        self.assertEqual(News.objects.get(id=id).newsline, False)
