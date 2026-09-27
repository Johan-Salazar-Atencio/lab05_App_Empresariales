from django.contrib import admin
from django.db.models import Q
from .models import Genre, Person, Movie, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    fields = ['user_name', 'score', 'comment']
    min_num = 0
    max_num = 5
    show_change_link = True


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


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
    inlines = [RatingInline]

    def get_main_genre(self, obj):
        genre = obj.genre.first()
        return genre.name if genre else '-'
    get_main_genre.short_description = 'Main Genre'

    def get_director_names(self, obj):
        if obj.director:
            return str(obj.director)
        return '-'
    get_director_names.short_description = 'Director'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.get_queryset(request).filter(
            Q(director__first_name__icontains=search_term) |
            Q(director__last_name__icontains=search_term)
        )
        return queryset, use_distinct

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user_name', 'score', 'comment', 'created_at']
    list_filter = ['score', 'movie']
    search_fields = ['movie__title', 'user_name']