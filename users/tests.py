from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse("user-register")
        payload = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "StrongPass123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_user_registration_without_email(self):
        url = reverse("user-register")
        payload = {
            "username": "no_email_user",
            "password": "StrongPass123",
            "telegram_chat_id": "12345678",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="no_email_user")
        self.assertEqual(user.email, "")
        self.assertEqual(user.telegram_chat_id, "12345678")

    def test_update_telegram_chat_id_after_registration(self):
        user = User.objects.create_user(username="telegram_user", password="StrongPass123")
        self.client.force_authenticate(user)

        response = self.client.patch(
            reverse("user-telegram-chat-id-update"),
            {"telegram_chat_id": "999777111"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.telegram_chat_id, "999777111")
