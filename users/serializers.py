from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True, allow_blank=False)
    telegram_chat_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "telegram_chat_id")

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class UserTelegramChatIdSerializer(serializers.ModelSerializer):
    telegram_chat_id = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("telegram_chat_id",)
