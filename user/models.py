from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    given_name = models.CharField(max_length=255)
    profile_image = models.ImageField(null=True, blank=True)
