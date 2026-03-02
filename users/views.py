from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import UserRegistrationSerializer, UserTelegramChatIdSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserTelegramChatIdUpdateView(generics.UpdateAPIView):
    serializer_class = UserTelegramChatIdSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
