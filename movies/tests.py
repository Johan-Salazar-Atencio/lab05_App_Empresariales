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
        genre = Genre.objects.create(name='Accion')
        self.assertEqual(str(genre), 'Accion')

    def test_genre_name_unique(self):
        Genre.objects.create(name='Accion')
        with self.assertRaises(Exception):
            Genre.objects.create(name='Accion')


class MovieModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Accion')
        self.movie = Movie.objects.create(
            title='El Origen',
            description='Un ladron que roba secretos corporativos',
            release_year=2010,
            duration_minutes=148,
            genre=self.genre,
            rating=4.8,
        )

    def test_create_movie(self):
        self.assertEqual(self.movie.title, 'El Origen')
        self.assertEqual(self.movie.release_year, 2010)
        self.assertEqual(float(self.movie.rating), 4.8)

    def test_movie_genre_relation(self):
        self.assertEqual(self.movie.genre, self.genre)

    def test_movie_poster_blank(self):
        movie = Movie.objects.create(
            title='Sin Poster', description='Prueba', release_year=2020,
            duration_minutes=90, genre=self.genre,
        )
        self.assertFalse(movie.poster)


class RecommendationModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Accion')
        self.movie = Movie.objects.create(
            title='El Origen', description='Prueba', release_year=2010,
            duration_minutes=148, genre=self.genre, rating=4.8,
        )
        self.rec = Recommendation.objects.create(
            movie=self.movie, user_name='admin', score=5, comment='Excelente',
        )

    def test_create_recommendation(self):
        self.assertEqual(self.rec.score, 5)
        self.assertEqual(self.rec.user_name, 'admin')

    def test_recommendation_relation(self):
        self.assertIn(self.rec, self.movie.recommendations.all())


@override_settings(DEBUG=False)
class PublicViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Accion')
        self.movie = Movie.objects.create(
            title='El Origen', description='Un ladron que roba secretos corporativos',
            release_year=2010, duration_minutes=148, genre=self.genre, rating=4.8,
        )
        Recommendation.objects.create(
            movie=self.movie, user_name='admin', score=5, comment='Excelente',
        )

    def test_movie_list_url(self):
        self.assertEqual(reverse('movies:movie_list'), '/')

    def test_movie_list_view(self):
        response = Client().get(reverse('movies:movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_list.html')

    def test_movie_detail_view(self):
        response = Client().get(reverse('movies:movie_detail', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_detail.html')

    def test_movie_create_view(self):
        response = Client().get(reverse('movies:movie_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_form.html')

    def test_movie_update_view(self):
        response = Client().get(reverse('movies:movie_update', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_form.html')

    def test_movie_delete_view(self):
        response = Client().get(reverse('movies:movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_confirm_delete.html')

    def test_search_filter(self):
        response = Client().get(reverse('movies:movie_list'), {'q': 'El Origen'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El Origen')

    def test_genre_filter(self):
        response = Client().get(reverse('movies:movie_list'), {'genre': self.genre.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El Origen')


class PermissionsTest(TestCase):
    def setUp(self):
        self.group, _ = Group.objects.get_or_create(name='editores')
        add_perm = Permission.objects.get(codename='add_movie')
        change_perm = Permission.objects.get(codename='change_movie')
        self.group.permissions.set([add_perm, change_perm])

        if not User.objects.filter(username='editor_user').exists():
            User.objects.create_user(username='editor_user', password='editor_password')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='admin_password')

    def test_editores_group_exists(self):
        self.assertTrue(Group.objects.filter(name='editores').exists())

    def test_editores_has_add_permission(self):
        group = Group.objects.get(name='editores')
        self.assertIn(Permission.objects.get(codename='add_movie'), group.permissions.all())

    def test_editores_has_change_permission(self):
        group = Group.objects.get(name='editores')
        self.assertIn(Permission.objects.get(codename='change_movie'), group.permissions.all())

    def test_editores_no_delete_permission(self):
        group = Group.objects.get(name='editores')
        self.assertEqual(group.permissions.filter(codename='delete_movie').count(), 0)
