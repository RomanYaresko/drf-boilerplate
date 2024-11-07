from http import HTTPMethod

from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from user.models import CustomUser
from user.serializers.custom_user import CustomUserLoginSerializer, CustomUserSerializer, CustomUserUpdateSerializer
from user.serializers.token import TokenSerializer


class CurrentCustomUserViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    RETRIEVE_ACTION_NAME = "retrieve"
    DESTROY_ACTION_NAME = "destroy"
    UPDATE_ACTION_NAME = "update"

    def get_object(self) -> CustomUser:
        return self.request.user

    def get_serializer_class(self) -> BaseSerializer:
        if self.action == CurrentCustomUserViewSet.UPDATE_ACTION_NAME:
            return CustomUserUpdateSerializer

        return CustomUserSerializer


class AuthCustomUserViewSet(GenericViewSet):
    queryset = CustomUser.objects.all()

    REGISTER_ACTION_NAME = "register"
    REGISTER_URL_PATH = "register"

    LOGIN_ACTION_NAME = "login"
    LOGIN_URL_PATH = "login"

    LOGOUT_ACTION_NAME = "logout"
    LOGOUT_URL_PATH = "logout"

    def get_permissions(self) -> list[BasePermission]:
        permissions = super().get_permissions()
        if self.action == AuthCustomUserViewSet.LOGOUT_ACTION_NAME:
            permissions.append(IsAuthenticated())

        return permissions

    def get_serializer_class(self) -> BaseSerializer | None:
        if self.action == AuthCustomUserViewSet.LOGIN_ACTION_NAME:
            return CustomUserLoginSerializer

        return CustomUserSerializer

    @action(methods=[HTTPMethod.POST.value], detail=False, url_path=REGISTER_URL_PATH)
    def register(self, request: HttpRequest) -> Response:
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        token = Token.objects.create(user=user)
        token_serializer = TokenSerializer(token)

        return Response(token_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=[HTTPMethod.POST.value], detail=False, url_path=LOGIN_URL_PATH)
    def login(self, request: HttpRequest) -> Response:
        login_serializer = self.get_serializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        token, _ = Token.objects.get_or_create(user=login_serializer.validated_data["user"])
        token_serializer = TokenSerializer(token)

        return Response(token_serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(methods=[HTTPMethod.POST.value], detail=False, url_path=LOGOUT_URL_PATH)
    def logout(self, request: HttpRequest) -> Response:
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist as err:
            msg = "User is not logged in"
            raise Exception(msg) from err

        return Response(status=status.HTTP_204_NO_CONTENT)
