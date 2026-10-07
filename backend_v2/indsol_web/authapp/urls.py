from django.urls import include, path
from rest_framework import routers

from authapp.views import (
    ProfileViewSet,
    UsersViewSet,
    DistrictsViewSet,
    PermissionViewSet,
    GroupViewSet,
    BranchesViewSet,
    ClientsViewSet,
    ManagersViewSet,
    PingView,
    AuthMailView,
    ReportMailView,
    GenerateNewPasswordViewSet,
    WikiPermissionViewSet,
    WikiGroupPermissionViewSet,
    WikiAdminListViewSet
)
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

auth = routers.DefaultRouter()
auth.register("permission", PermissionViewSet, basename='permission')
auth.register("groups", GroupViewSet, basename='groups')
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
auth.register("change_password", GenerateNewPasswordViewSet, basename="change_password")  # Смена пароля
auth.register("wiki_permissions", WikiPermissionViewSet, basename="wiki_permissions") # Разрешения вики
auth.register("wiki_group_permissions", WikiGroupPermissionViewSet, basename="wiki_group_permissions") # Группы разрешений вики
auth.register("wiki_admin_list", WikiAdminListViewSet, basename="wiki_admin_list") # список вики для вывода в разрешениях


urlpatterns = [
    path("", include(auth.urls)),
    path("ping/", PingView.as_view(), name="ping"),  # Пинг сервера
    #path("permission/", PermissionViewSet, name="permission"), # Разрешения
    #path('groups', GroupViewSet, name="groups"), # Группы
    #path(
    #    "reg_request/", AuthMailView, name="reg_request"
    #),  # Отправка данных регистрации менеджерам
    #path(
    #    "report/", ReportMailView, name="report"
    #),  # Отправка данных о пользовательских отчетах
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
