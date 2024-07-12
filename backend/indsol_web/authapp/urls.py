from django.urls import include, path
from rest_framework import routers

from authapp.views import (
    ProfileViewSet,
    UsersViewSet,
    PingViewSet,
    DistrictsViewSet,
    BranchesViewSet,
    ContractsSerializers,
    ClientsViewSet,
    ManagersViewSet,
)
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

auth = routers.DefaultRouter()
auth.register("users", UsersViewSet, basename="users")
auth.register("profile", ProfileViewSet, basename="profile")
auth.register("districts", DistrictsViewSet, basename="districts")
auth.register("branches", BranchesViewSet, basename="branches")
auth.register("contracts", ContractsSerializers, basename="contracts")
auth.register("clients", ClientsViewSet, basename="clients")
auth.register("managers", ManagersViewSet, basename="managers")


urlpatterns = [
    path("", include(auth.urls)),
    path("ping/", PingViewSet.as_view(), name="ping"),
    path("debug/", include("rest_framework.urls")),
    path(
        "token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
