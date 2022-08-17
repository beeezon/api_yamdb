from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser', 'is_staff', 'moderator')


admin.site.register(User, UserAdmin)