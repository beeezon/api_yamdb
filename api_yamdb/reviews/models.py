from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):

    USER_STATUS = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]

    email = models.EmailField(max_length=254, blank=False)
    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=USER_STATUS, default='user', max_length=10)


class Category(models.Model):
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=50, unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles')

class Genre(models.Model):
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=50, unique=True)


class Reviews(models.Model):
    title_id = models.ForeignKey(
        Titles, 
        on_delete=models.CASCADE, 
        related_name='titles')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])


class Comment(models.Model):
    review_id = models.ForeignKey(
        Reviews, 
        on_delete=models.CASCADE, 
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

