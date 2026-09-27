from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import Group, User, Permission
from django.template.context import Context
from .models import Genre, Movie, Recommendation


def _patch_context_copy():
    def __copy__(self):
        duplicate = Context()
        duplicate.dicts = self.dicts[:]
        return duplicate
    Context.__copy__ = __copy__


_patch_context_copy()


class GenreModelTest(TestCase):
    def test_create_genre(self):
        genre = Genre.objects.create(name='Action')
        self.assertEqual(str(genre), 'Action')
        self.assertEqual(genre.name, 'Action')

    def test_genre_name_unique(self):
        Genre.objects.create(name='Action')
        with self.assertRaises(Exception):
            Genre.objects.create(name='Action')

    def test_genre_db_table(self):
        genre = Genre.objects.create(name='SciFi')
        self.assertEqual(Genre._meta.db_table, 'genres')


class MovieModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Inception',
            description='A dream heist film',
            release_year=2010,
            duration_minutes=148,
            genre=self.genre,
            rating=4.8,
        )

    def test_create_movie(self):
        self.assertEqual(str(self.movie), 'Inception (2010)')
        self.assertEqual(self.movie.title, 'Inception')
        self.assertEqual(self.movie.release_year, 2010)
        self.assertEqual(self.movie.duration_minutes, 148)
        self.assertEqual(float(self.movie.rating), 4.8)

    def test_movie_genre_relation(self):
        self.assertEqual(self.movie.genre, self.genre)
        self.assertIn(self.movie, self.genre.movies.all())

    def test_movie_poster_blank(self):
        movie_no_poster = Movie.objects.create(
            title='No Poster',
            description='Test',
            release_year=2020,
            duration_minutes=90,
            genre=self.genre,
        )
        self.assertFalse(movie_no_poster.poster)

    def test_movie_db_table(self):
        self.assertEqual(Movie._meta.db_table, 'movies')

    def test_movie_ordering(self):
        Movie.objects.create(
            title='Older Movie',
            description='Test',
            release_year=2000,
            duration_minutes=100,
            genre=self.genre,
        )
        movies = list(Movie.objects.all())
        self.assertEqual(movies[0].title, 'Inception')
        self.assertEqual(movies[1].title, 'Older Movie')


class RecommendationModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Inception',
            description='A dream heist',
            release_year=2010,
            duration_minutes=148,
            genre=self.genre,
            rating=4.8,
        )
        self.recommendation = Recommendation.objects.create(
            movie=self.movie,
            user_name='admin',
            score=5,
            comment='Excellent',
        )

    def test_create_recommendation(self):
        self.assertEqual(str(self.recommendation), 'admin - Inception (5/5)')
        self.assertEqual(self.recommendation.score, 5)
        self.assertEqual(self.recommendation.comment, 'Excellent')

    def test_recommendation_relation(self):
        self.assertIn(self.recommendation, self.movie.recommendations.all())
        self.assertEqual(self.movie.recommendations.count(), 1)

    def test_recommendation_db_table(self):
        self.assertEqual(Recommendation._meta.db_table, 'recommendations')


class MovieAdminTest(TestCase):
    def setUp(self):
        from django.contrib.admin.sites import AdminSite
        from .admin import MovieAdmin, GenreAdmin, RecommendationAdmin, RecommendationInline

        self.site = AdminSite()
        self.genre_admin = GenreAdmin(Genre, self.site)
        self.movie_admin = MovieAdmin(Movie, self.site)
        self.rec_admin = RecommendationAdmin(Recommendation, self.site)
        self.user = User.objects.create_user(username='testuser')

    def test_genre_admin_list_display(self):
        self.assertIn('name', self.genre_admin.list_display)

    def test_genre_admin_search_fields(self):
        self.assertEqual(self.genre_admin.search_fields, ['name'])

    def test_movie_admin_list_display(self):
        self.assertIn('title', self.movie_admin.list_display)
        self.assertIn('release_year', self.movie_admin.list_display)
        self.assertIn('genre', self.movie_admin.list_display)
        self.assertIn('rating', self.movie_admin.list_display)

    def test_movie_admin_list_filter(self):
        self.assertIn('genre', self.movie_admin.list_filter)
        self.assertIn('release_year', self.movie_admin.list_filter)

    def test_movie_admin_search_fields(self):
        self.assertIn('title', self.movie_admin.search_fields)
        self.assertIn('description', self.movie_admin.search_fields)

    def test_movie_admin_readonly_fields(self):
        self.assertEqual(self.movie_admin.readonly_fields, ['created_at', 'updated_at'])

    def test_movie_admin_inlines(self):
        from .admin import RecommendationInline
        self.assertIn(RecommendationInline, self.movie_admin.inlines)

    def test_recommendation_admin_list_display(self):
        self.assertIn('movie', self.rec_admin.list_display)
        self.assertIn('user_name', self.rec_admin.list_display)
        self.assertIn('score', self.rec_admin.list_display)

    def test_recommendation_admin_search_fields(self):
        self.assertIn('movie__title', self.rec_admin.search_fields)
        self.assertIn('user_name', self.rec_admin.search_fields)


class RecommendationInlineTest(TestCase):
    def setUp(self):
        from django.contrib.admin.sites import AdminSite
        from .admin import RecommendationInline
        self.site = AdminSite()
        self.inline = RecommendationInline(Recommendation, self.site)

    def test_inline_model(self):
        self.assertEqual(self.inline.model, Recommendation)

    def test_inline_fields(self):
        self.assertEqual(self.inline.fields, ['user_name', 'score', 'comment'])


@override_settings(DEBUG=False)
class PublicViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Inception',
            description='A dream heist film',
            release_year=2010,
            duration_minutes=148,
            genre=self.genre,
            rating=4.8,
        )
        Recommendation.objects.create(
            movie=self.movie,
            user_name='admin',
            score=5,
            comment='Excellent',
        )

    def test_recommendations_url(self):
        url = reverse('movies:recommendations')
        self.assertEqual(url, '/recommendations/')

    def test_recommendations_view_status(self):
        client = Client()
        response = client.get(reverse('movies:recommendations'))
        self.assertEqual(response.status_code, 200)

    def test_recommendations_template(self):
        client = Client()
        response = client.get(reverse('movies:recommendations'))
        self.assertTemplateUsed(response, 'movies/recommendations.html')

    def test_recommendations_contains_movies(self):
        client = Client()
        response = client.get(reverse('movies:recommendations'))
        self.assertContains(response, 'Inception')

    def test_recommendations_has_genres(self):
        client = Client()
        response = client.get(reverse('movies:recommendations'))
        self.assertContains(response, 'Action')

    def test_recommendations_context_data(self):
        client = Client()
        response = client.get(reverse('movies:recommendations'))
        self.assertIn('genre_data', response.context)
        self.assertGreater(len(response.context['genre_data']), 0)
        first_entry = response.context['genre_data'][0]
        self.assertIn('genre', first_entry)
        self.assertIn('movies', first_entry)


class PermissionsTest(TestCase):
    def setUp(self):
        self.group, _ = Group.objects.get_or_create(name='editores')
        add_perm = Permission.objects.get(codename='add_movie')
        change_perm = Permission.objects.get(codename='change_movie')
        self.group.permissions.set([add_perm, change_perm])

        if not User.objects.filter(username='editor_user').exists():
            User.objects.create_user(
                username='editor_user',
                email='editor@example.com',
                password='editor_password'
            )

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin_password'
            )

    def test_editores_group_exists(self):
        group = Group.objects.get(name='editores')
        self.assertEqual(group.name, 'editores')

    def test_editores_has_add_permission(self):
        group = Group.objects.get(name='editores')
        self.assertIn(Permission.objects.get(codename='add_movie'), group.permissions.all())

    def test_editores_has_change_permission(self):
        group = Group.objects.get(name='editores')
        self.assertIn(Permission.objects.get(codename='change_movie'), group.permissions.all())

    def test_editores_no_delete_permission(self):
        group = Group.objects.get(name='editores')
        delete_perms = group.permissions.filter(codename='delete_movie')
        self.assertEqual(delete_perms.count(), 0)

    def test_editor_user_exists(self):
        self.assertTrue(User.objects.filter(username='editor_user').exists())

    def test_admin_user_exists(self):
        self.assertTrue(User.objects.filter(username='admin').exists())
        admin = User.objects.get(username='admin')
        self.assertTrue(admin.is_superuser)
