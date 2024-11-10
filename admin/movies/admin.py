from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork, User, Template, Content, Event


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('film_work', 'person', )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, )

    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')

    list_filter = ('type', )

    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline, )
    search_fields = ('full_name', )

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('created', 'modified')
    search_fields = ('template', )


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('created', 'modified')
    search_fields = ('words', )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'template_id', 'content_id', 'timestamp', 'created', 'modified')
    search_fields = ('template__template_id', 'content__content_id', 'users')
