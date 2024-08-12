from django.urls import include, path
from rest_framework import routers

from authapp.views import (
    ProfileViewSet,
    UsersViewSet,
    DistrictsViewSet,
    BranchesViewSet,
    ClientsViewSet,
    ManagersViewSet,
    PingView,
    AuthMailView,
)
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

auth = routers.DefaultRouter()
auth.register("users", UsersViewSet, basename="users")  # Список пользователей
auth.register(
    "profile", ProfileViewSet, basename="profile"
)  # Профиль текущего пользователя
auth.register("districts", DistrictsViewSet, basename="districts")  # Список регионов
auth.register(
    "branches", BranchesViewSet, basename="branches"
)  # Список производственных отралсей
auth.register("clients", ClientsViewSet, basename="clients")  # Список клиентов
auth.register("managers", ManagersViewSet, basename="managers")  # Список менеджеров

urlpatterns = [
    path("", include(auth.urls)),
    path("ping/", PingView.as_view(), name="ping"),  # Пинг сервера
    path(
        "send_mail/", AuthMailView, name="send_mail"
    ),  # Отправка данный реггистрации менеджерам
    path("debug/", include("rest_framework.urls")),  # Дебаг режим
    path(
        "token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),  # Получение JWT токена
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),  # Обновление JWT токена по refresh токену
]
