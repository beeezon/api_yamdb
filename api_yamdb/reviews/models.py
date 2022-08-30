from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import current_year_validator


class Users(AbstractUser):

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


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'


class Titles(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Наменование')
    year = models.IntegerField(
        verbose_name='Год выпуска', validators=[current_year_validator])
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles')
    genre = models.ManyToManyField(
        Genres,
        related_name="titles",
        verbose_name="Жанр произведения",
    )
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название'
        ordering = ['name']


class GenresTitles(models.Model):
    title = models.ForeignKey(
        Titles, verbose_name='Название', on_delete=models.CASCADE)    
    genre = models.ForeignKey(
        Genres, verbose_name='Жанр', on_delete=models.CASCADE)

    def __str__(self):
        return self.genre, self.title

    class Meta:
        verbose_name = 'Жанр и название'


class Reviews(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title_id", "author"], name="unique_review"
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
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
