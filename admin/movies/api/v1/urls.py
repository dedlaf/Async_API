from django.urls import path

from movies.api.v1 import views


urlpatterns = [
    path('movies/', views.MoviesListApi.as_view()),
    path('movies/<str:pk>', views.MoviesDetailApi.as_view())
]
