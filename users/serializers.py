from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=False, allow_blank=True)
    telegram_chat_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "telegram_chat_id")

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.setdefault("email", "")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserTelegramChatIdSerializer(serializers.ModelSerializer):
    telegram_chat_id = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("telegram_chat_id",)
