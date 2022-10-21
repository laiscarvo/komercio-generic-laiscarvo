from django.contrib import admin

"""from django.contrib.auth.admin import UserAdmin

from .models import Account


class CustomAccountAdmin(UserAdmin):
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (
            "Credentials",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name"),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_superuser", "is_seller", "is_active"),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("date_joined", "last_login"),
            },
        ),
    )


admin.site.register(Account, CustomAccountAdmin)
 """
