from django.contrib import admin
from .models import Genre, Movie, Recommendation


class RecommendationInline(admin.TabularInline):
    model = Recommendation
    extra = 1
    fields = ['user_name', 'score', 'comment']
    min_num = 0
    max_num = 10
    show_change_link = True


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie_count']
    search_fields = ['name']

    def movie_count(self, obj):
        return obj.movies.count()
    movie_count.short_description = 'Movies'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'genre', 'rating', 'duration_minutes', 'created_at']
    list_filter = ['genre', 'release_year']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RecommendationInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'release_year')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'genre', 'rating', 'poster')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user_name', 'score', 'created_at']
    list_filter = ['score', 'movie']
    search_fields = ['movie__title', 'user_name']
