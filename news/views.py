from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def index(request):
    articles = Article.objects.all().order_by('-published_at')
    categories = Category.objects.all().order_by('name')

    context = {
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'news/index.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    categories = Category.objects.all().order_by('name')

    context = {
        'article': article,
        'categories': categories,
    }
    return render(request, 'news/article_detail.html', context)


def category_articles(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles = Article.objects.filter(categories=category).order_by('-published_at')
    categories = Category.objects.all().order_by('name')

    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'news/category_articles.html', context)
