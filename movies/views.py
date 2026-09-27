from django.shortcuts import render
from .models import Genre, Movie


def movie_recommendations(request):
    genres = Genre.objects.all().order_by('name')

    genre_data = []
    for genre in genres:
        movies = Movie.objects.filter(genre=genre).order_by('-rating')
        genre_data.append({
            'genre': genre,
            'movies': movies,
        })

    context = {
        'genre_data': genre_data,
    }
    return render(request, 'movies/recommendations.html', context)
