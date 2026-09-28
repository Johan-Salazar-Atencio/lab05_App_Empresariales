from django.contrib import admin
from django.db.models import Q
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
    movie_count.short_description = 'Peliculas'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'genre', 'rating', 'duration_minutes', 'created_at']
    list_filter = ['genre', 'release_year']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RecommendationInline]
    fieldsets = (
        ('Informacion Basica', {
            'fields': ('title', 'description', 'release_year')
        }),
        ('Detalles', {
            'fields': ('duration_minutes', 'genre', 'rating', 'poster')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.get_queryset(request).filter(
            Q(genre__name__icontains=search_term)
        )
        return queryset, use_distinct


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user_name', 'score', 'created_at']
    list_filter = ['score', 'movie', 'created_at']
    search_fields = ['movie__title', 'user_name', 'comment']
