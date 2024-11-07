from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.serializers.custom_user import CustomUserSerializer


class TokenSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ["key", "user"]
