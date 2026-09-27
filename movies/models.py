from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='covers/', blank=True, null=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='movies',
    )
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movies'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Recommendation(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='recommendations',
    )
    user_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    score = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommendations'
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} - {self.movie.title} ({self.score}/5)"
