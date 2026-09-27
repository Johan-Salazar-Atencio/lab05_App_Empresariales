from django.contrib import admin
from .models import Genre, Person, Movie, Rating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'role', 'created_at']
    list_filter = ['role']
    search_fields = ['first_name', 'last_name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'get_main_genre', 'get_director_names', 'created_at']
    list_filter = ['genre', 'release_year']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']

    def get_main_genre(self, obj):
        genre = obj.genre.first()
        return genre.name if genre else '-'
    get_main_genre.short_description = 'Main Genre'

    def get_director_names(self, obj):
        if obj.director:
            return str(obj.director)
        return '-'
    get_director_names.short_description = 'Director'

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user_name', 'score', 'created_at']
    list_filter = ['score', 'movie']
    search_fields = ['movie__title', 'user_name']