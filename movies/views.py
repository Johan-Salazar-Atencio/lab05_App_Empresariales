from django.shortcuts import render, get_object_or_404
from .models import Genre, Movie


def movie_list(request):
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
    return render(request, 'movies/movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    recommendations = movie.recommendations.all()

    context = {
        'movie': movie,
        'recommendations': recommendations,
    }
    return render(request, 'movies/movie_detail.html', context)
