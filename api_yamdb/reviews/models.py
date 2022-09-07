from tabnanny import verbose
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


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


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
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

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class CommentReview(models.Model):
    text = models.TextField(verbose_name = 'Текст ревью или коммента')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Reviews(CommentReview):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name = 'Отзыв',
        related_name='reviews')
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name = 'Отзыв пользователя',
        related_name='reviews')
    score = models.SmallIntegerField(
        verbose_name = 'Оценка',
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title_id"], name="unique_titile_author"
            )
        ]

    def __str__(self):
        return self.name


class Comments(CommentReview):
    review_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        verbose_name = 'Комментарий',
        related_name='comments')
    author = models.ForeignKey(
        Users,
        verbose_name = 'Комментарий пользователя',
        on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
