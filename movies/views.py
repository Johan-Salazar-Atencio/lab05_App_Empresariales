from django.shortcuts import render
from .models import Genre, Movie
from django.db.models import Avg


def movie_recommendations(request):
    genres = Genre.objects.annotate(avg_rating=Avg('movies__ratings__score')).order_by('-avg_rating')

    recommendations = {}
    for genre in genres:
        movies = Movie.objects.filter(genre=genre).annotate(
            avg_score=Avg('ratings__score')
        ).order_by('-avg_score')
        recommendations[genre] = movies

    context = {
        'genres': genres,
        'recommendations': recommendations,
    }
    return render(request, 'movies/recommendations.html', context)
