from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Genre, Movie, Recommendation
from .forms import MovieForm, RecommendationForm


def movie_list(request):
    query = request.GET.get('q', '')
    genre_filter = request.GET.get('genre', '')

    genres = Genre.objects.all().order_by('name')

    movies = Movie.objects.all().order_by('-rating')
    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if genre_filter:
        movies = movies.filter(genre_id=genre_filter)

    genre_data = []
    for genre in genres:
        genre_movies = movies.filter(genre=genre)
        genre_data.append({
            'genre': genre,
            'movies': genre_movies,
        })

    context = {
        'genre_data': genre_data,
        'genres': genres,
        'query': query,
        'selected_genre': genre_filter,
    }
    return render(request, 'movies/movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    recommendations = movie.recommendations.all().order_by('-created_at')

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.movie = movie
            rec.save()
            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = RecommendationForm()

    context = {
        'movie': movie,
        'recommendations': recommendations,
        'form': form,
    }
    return render(request, 'movies/movie_detail.html', context)


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/movie_form.html', {
        'form': form,
        'title': 'Add Movie',
    })


def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/movie_form.html', {
        'form': form,
        'title': 'Edit Movie',
        'movie': movie,
    })


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:movie_list')

    return render(request, 'movies/movie_confirm_delete.html', {
        'movie': movie,
    })
