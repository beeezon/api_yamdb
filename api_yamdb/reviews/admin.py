from django.contrib import admin

from reviews.models import Categories, Genres, Titles

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
