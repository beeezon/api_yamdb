from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
        verbose_name="Жанр произведения",
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
