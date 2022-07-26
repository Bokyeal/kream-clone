from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",  # 어드민페이지 상단 바 이름
            {
                "fields": (
                    "avatar",
                    "phone_number",
                    "shoe_size",
                    "is_ad_message",
                    "is_ad_email",
                )
            },
        ),
    )
