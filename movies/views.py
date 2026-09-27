from django.shortcuts import render
from django.db.models import Avg
from .models import Genre, Movie


def movie_recommendations(request):
    genres = Genre.objects.annotate(
        avg_rating=Avg('movies__ratings__score')
    ).order_by('-avg_rating')

    genre_data = []
    for genre in genres:
        movies = Movie.objects.filter(genre=genre).annotate(
            avg_score=Avg('ratings__score')
        ).order_by('-avg_score')
        genre_data.append({
            'genre': genre,
            'movies': movies,
        })

    context = {
        'genre_data': genre_data,
    }
    return render(request, 'movies/recommendations.html', context)
