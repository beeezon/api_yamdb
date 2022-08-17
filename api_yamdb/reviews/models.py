from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    moderator = models.BooleanField('Модератор', default=False)
    email = models.EmailField('email адрес', unique=True)
