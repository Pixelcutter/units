from django.urls import path
from .views import RegisterUnitsUserView, UnitsUserDetail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterUnitsUserView.as_view(), name="register_user"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("<int:pk>/", UnitsUserDetail.as_view(), name="user_detail"),
]
