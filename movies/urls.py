from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('recommendations/', views.movie_recommendations, name='recommendations'),
]
