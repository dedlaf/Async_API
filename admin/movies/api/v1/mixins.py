from django.contrib.postgres.aggregates import ArrayAgg

from django.db.models import Q, Count, OuterRef, Subquery
from django.http import JsonResponse

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        genres_subquery = (Filmwork.objects.filter(id=OuterRef('id')).annotate(genre_names=ArrayAgg('genres__name')).values('genre_names'))
        actors_subquery = (Filmwork.objects.filter(id=OuterRef('id'))
                           .annotate(actor_names=ArrayAgg('personfilmwork__person__full_name')).values('actor_names'))

        queryset = (Filmwork.objects.prefetch_related('genres', 'persons')
                    .values('id', 'title', 'description', 'creation_date', 'rating', 'type')
                    .annotate(genres=Subquery(genres_subquery),
                              actors=Subquery(actors_subquery),))
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
