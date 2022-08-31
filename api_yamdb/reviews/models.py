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
    username = models.CharField(
        max_length=50,
        unique=True
    )


    @property
    def is_admin(self):
        return self.is_superuser or self.role == "admin" or self.is_staff

    @property
    def is_moder(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'


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
    name = models.CharField(max_length=200, verbose_name='Наименование')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genres,
        related_name="titles",
        blank=True,
        verbose_name='Жанр',
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        verbose_name='Рейтинг'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'


class GenresTitles(models.Model):
    genre_id = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Наименование'
    )

    def __str__(self):
        return self.title_id, self.genre_id

    class Meta:
        verbose_name = 'Наименование и Жанр'


class Reviews(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Наименование'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Рейтинг'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title_id", "author"], name="unique_review"
            ),
        ],
        verbose_name = 'Отзыв',
        ordering = ["pub_date"]

    def __str__(self):
        return self.text


class Comments(models.Model):
    review_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ["pub_date"],
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text
