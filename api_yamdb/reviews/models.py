from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import year_validation

class Users(AbstractUser):

    USER_STATUS = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]

    email = models.EmailField(max_length=254, blank=False, unique=True)
    bio = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(choices=USER_STATUS, default='user', max_length=10)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_moder(self):
        return self.role == 'moderator'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ['id']


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[year_validation])
    description = models.TextField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genres,
        related_name="titles",
        blank=True,
        verbose_name="Жанр произведения",
    )
    rating = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class GenresTitles(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title, self.genre


class Reviews(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, db_index = True)
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            ),
        ]


class Comments(models.Model):
    review_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["pub_date"]
