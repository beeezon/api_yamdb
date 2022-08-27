from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Categories, Genres, Titles


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active')


admin.site.register(Users, UserAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
