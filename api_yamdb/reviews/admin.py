from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GenresTitles, Reviews, Users, Categories, Genres, Titles, Comments


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')


admin.site.register(Users, UserAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
admin.site.register(GenresTitles)
admin.site.register(Reviews)
admin.site.register(Comments)
