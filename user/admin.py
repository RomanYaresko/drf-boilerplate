from typing import Any

from django.contrib import admin
from django.utils.html import format_html

from user.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = [
        "username",
        "given_name",
        "profile_image_tag",
    ]

    def profile_image_tag(self, obj: CustomUser) -> Any:
        return format_html(
            f'<img src="{obj.profile_image.url if obj.profile_image else ''}" style="max-width:50px; max-height:50px"/>'
        )


admin.site.register(CustomUser, CustomUserAdmin)
