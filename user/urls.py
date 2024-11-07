from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views.custom_user import AuthCustomUserViewSet, CurrentCustomUserViewSet

router = DefaultRouter()
router.register("auth", AuthCustomUserViewSet)

urlpatterns = [
    path("current/", CurrentCustomUserViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"})),
    path("", include(router.urls)),
]
