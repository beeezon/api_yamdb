from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):

    USER_STATUS = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]

    email = models.EmailField(max_length=254, blank=False, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=USER_STATUS, default='user', max_length=10)
    is_active = models.BooleanField(
        ('active'),
        default=True,
    )


    @property
    def is_admin(self):
        return self.is_superuser or self.role == "admin" or self.is_staff

    @property
    def is_moder(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='title')
    genre = models.ManyToManyField(
        Genre,
        related_name="title",
        blank=True,
        verbose_name="Жанр произведения",
    )


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title_id", "author"], name="unique_review"
            ),
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
