from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Users, Categories, Genres, Titles, GenresTitles, Comments, Reviews)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active')


admin.site.register(Users, UserAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
admin.site.register(GenresTitles)
admin.site.register(Comments)
admin.site.register(Reviews)
