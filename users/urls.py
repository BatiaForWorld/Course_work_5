from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserRegistrationView, UserTelegramChatIdUpdateView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("telegram-chat-id/", UserTelegramChatIdUpdateView.as_view(), name="user-telegram-chat-id-update"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
