from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Person(models.Model):
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('actor', 'Actor'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='actor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'people'
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    synopsis = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='movies', blank=True)
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directed_movies',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movies'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-release_year', '-created_at']

    def __str__(self):
        return self.title


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    score = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    user_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ratings'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} - {self.movie.title} ({self.score}/5)"
