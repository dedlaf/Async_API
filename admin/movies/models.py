import json
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .mixins import TimeStampedMixin, UUIDMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return f'{self.email} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "content\".\"user"



class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        managed = False
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Types(models.TextChoices):
        MOVIES = _('MOVIES')
        TV_SHOWS = _('TV SHOWS')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), choices=Types.choices, default=Types.MOVIES)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        managed = False
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full name', max_length=512)

    class Meta:
        managed = False
        db_table = "content\".\"person"
        verbose_name = _('actor')
        verbose_name_plural = _('actors')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    class Roles(models.TextChoices):
        ACTOR = 'Actor'
        PRODUCER = 'Producer'
        DIRECTOR = 'Director'

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=Roles.choices, default=Roles.ACTOR)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "content\".\"person_film_work"


class Template(UUIDMixin, TimeStampedMixin):
    template_name = models.CharField(_('template name'), max_length=255)
    template = models.TextField(verbose_name=_('template'))

    class Meta:
        db_table = "notify\".\"template"
        verbose_name = _('template')
        verbose_name_plural = _('templates')

    def __str__(self):
        return f'Template {self.template_name}'


class Content(UUIDMixin, TimeStampedMixin):
    def validate_json_format(value):
        try:
            # Если значение уже является словарем, преобразуем его в строку JSON
            if isinstance(value, dict):
                value = json.dumps(value)
            json.loads(value)
        except ValueError as e:
            raise ValidationError(f'Invalid JSON: {e}')

    words = models.JSONField(_('Word List'), validators=[validate_json_format])

    class Meta:
        db_table = "notify\".\"content"
        verbose_name = _('content')
        verbose_name_plural = _('contents')

    def __str__(self):
        return f'Content {self.id}'

class Event(UUIDMixin, TimeStampedMixin):
    template = models.ForeignKey('Template', on_delete=models.CASCADE, related_name='events')
    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='events')
    users = ArrayField(models.UUIDField(), verbose_name=_('Users List'))
    timestamp = models.DateTimeField(_('Timestamp (UTC)'))

    class Meta:
        db_table = "notify\".\"event"
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return f'Event {self.id}'
