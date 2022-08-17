from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=200)
    id_key = models.SlugField(max_length=10, unique=True)

    def __str__(self):
        return self.name
