from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Genre, Title


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active')


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
