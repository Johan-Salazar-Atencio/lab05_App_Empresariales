from django.contrib import admin
from .models import Author, Category, Article


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'created_at']
    search_fields = ['name', 'bio']
    readonly_fields = ['created_at', 'updated_at']

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articulos'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articulos'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_at', 'category_list']
    list_filter = ['categories', 'published_at', 'author']
    search_fields = ['title', 'body', 'summary']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['categories']
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'summary', 'body')
        }),
        ('Multimedia', {
            'fields': ('image',)
        }),
        ('Relaciones', {
            'fields': ('author', 'categories')
        }),
        ('Fechas', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def category_list(self, obj):
        return ', '.join([c.name for c in obj.categories.all()])
    category_list.short_description = 'Categorias'
