from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, User


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Review)
