from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    given_name = serializers.CharField()
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "given_name",
            "profile_image",
        ]

    def validate_password(self, value: str) -> str:
        return make_password(value)


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    given_name = serializers.CharField()
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "given_name",
            "profile_image",
        ]


class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(request=self.context.get("request"), username=username, password=password)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data
