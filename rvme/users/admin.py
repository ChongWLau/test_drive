from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import User


@register(User)
class UserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'last_login', 'date_joined',
    ]
    search_fields = [
        'email',
    ]
