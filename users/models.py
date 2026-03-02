from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=64, blank=True, null=True, verbose_name="Telegram chat id"
    )
