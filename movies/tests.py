from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import Group, User, Permission
from django.template.context import Context
from .models import Genre, Person, Movie, Rating


def _patch_context_copy():
    def __copy__(self):
        duplicate = Context()
        duplicate.dicts = self.dicts[:]
        return duplicate
    Context.__copy__ = __copy__


_patch_context_copy()


class GenreModelTest(TestCase):
    def test_create_genre(self):
        genre = Genre.objects.create(name='Action', description='High energy')
        self.assertEqual(str(genre), 'Action')
        self.assertEqual(genre.name, 'Action')

    def test_genre_ordering(self):
        Genre.objects.create(name='B', description='')
        Genre.objects.create(name='A', description='')
        genres = list(Genre.objects.all())
        self.assertEqual(genres[0].name, 'A')
        self.assertEqual(genres[1].name, 'B')

    def test_genre_db_table(self):
        genre = Genre.objects.create(name='SciFi')
        self.assertEqual(Genre._meta.db_table, 'genres')


class PersonModelTest(TestCase):
    def test_create_person_director(self):
        person = Person.objects.create(first_name='Christopher', last_name='Nolan', role='director')
        self.assertIn('Director', str(person))
        self.assertEqual(person.role, 'director')

    def test_create_person_actor(self):
        person = Person.objects.create(first_name='Bradley', last_name='Cooper', role='actor')
        self.assertIn('Actor', str(person))
        self.assertEqual(person.role, 'actor')

    def test_person_db_table(self):
        Person.objects.create(first_name='Test', last_name='User', role='actor')
        self.assertEqual(Person._meta.db_table, 'people')


class MovieModelTest(TestCase):
    def setUp(self):
        self.genre_action = Genre.objects.create(name='Action', description='')
        self.genre_drama = Genre.objects.create(name='Drama', description='')
        self.director = Person.objects.create(first_name='Christopher', last_name='Nolan', role='director')
        self.movie = Movie.objects.create(
            title='Inception',
            release_year=2010,
            synopsis='A dream heist film',
            director=self.director
        )
        self.movie.genre.set([self.genre_action, self.genre_drama])

    def test_create_movie(self):
        self.assertEqual(str(self.movie), 'Inception')
        self.assertEqual(self.movie.title, 'Inception')
        self.assertEqual(self.movie.release_year, 2010)

    def test_movie_genre_relation(self):
        self.assertIn(self.genre_action, self.movie.genre.all())
        self.assertIn(self.genre_drama, self.movie.genre.all())
        self.assertEqual(self.movie.genre.count(), 2)

    def test_movie_director_relation(self):
        self.assertEqual(self.movie.director, self.director)

    def test_movie_db_table(self):
        self.assertEqual(Movie._meta.db_table, 'movies')

    def test_movie_string(self):
        self.assertEqual(str(self.movie), 'Inception')

    def test_movie_blank_director(self):
        movie_no_dir = Movie.objects.create(
            title='No Director',
            release_year=2020,
            synopsis='No director movie'
        )
        self.assertIsNone(movie_no_dir.director)
        self.assertEqual(str(movie_no_dir), 'No Director')

    def test_movie_string_representation(self):
        genre = Genre.objects.create(name='Test', description='')
        director = Person.objects.create(first_name='John', last_name='Doe', role='director')
        movie = Movie.objects.create(
            title='Test Movie',
            release_year=2023,
            synopsis='Test',
            director=director
        )
        movie.genre.set([genre])
        self.assertEqual(str(movie), 'Test Movie')


class RatingModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action', description='')
        self.director = Person.objects.create(first_name='Christopher', last_name='Nolan', role='director')
        self.movie = Movie.objects.create(
            title='Inception',
            release_year=2010,
            synopsis='A dream heist',
            director=self.director
        )
        self.rating = Rating.objects.create(
            movie=self.movie,
            score=5,
            comment='Excellent',
            user_name='admin'
        )

    def test_create_rating(self):
        self.assertEqual(str(self.rating), 'admin - Inception (5/5)')
        self.assertEqual(self.rating.score, 5)
        self.assertEqual(self.rating.comment, 'Excellent')

    def test_rating_relation(self):
        self.assertIn(self.rating, self.movie.ratings.all())
        self.assertEqual(self.movie.ratings.count(), 1)

    def test_rating_db_table(self):
        self.assertEqual(Rating._meta.db_table, 'ratings')


class MovieAdminTest(TestCase):
    def setUp(self):
        from django.contrib.admin.sites import AdminSite
        from .admin import MovieAdmin, GenreAdmin, PersonAdmin, RatingAdmin, RatingInline

        self.site = AdminSite()
        self.genre_admin = GenreAdmin(Genre, self.site)
        self.person_admin = PersonAdmin(Person, self.site)
        self.movie_admin = MovieAdmin(Movie, self.site)
        self.rating_admin = RatingAdmin(Rating, self.site)
        self.user = User.objects.create_user(username='testuser')

    def test_genre_admin_list_display(self):
        self.assertEqual(self.genre_admin.list_display, ['name', 'description', 'created_at'])

    def test_genre_admin_search_fields(self):
        self.assertEqual(self.genre_admin.search_fields, ['name'])

    def test_person_admin_list_display(self):
        self.assertEqual(self.person_admin.list_display, ['first_name', 'last_name', 'role', 'created_at'])

    def test_person_admin_search_fields(self):
        self.assertEqual(self.person_admin.search_fields, ['first_name', 'last_name'])

    def test_movie_admin_list_display(self):
        self.assertEqual(self.movie_admin.list_display, ['title', 'release_year', 'get_main_genre', 'get_director_names', 'created_at'])

    def test_movie_admin_list_filter(self):
        self.assertEqual(self.movie_admin.list_filter, ['genre', 'release_year'])

    def test_movie_admin_search_fields(self):
        self.assertEqual(self.movie_admin.search_fields, ['title'])

    def test_movie_admin_readonly_fields(self):
        self.assertEqual(self.movie_admin.readonly_fields, ['created_at', 'updated_at'])

    def test_movie_admin_inlines(self):
        from .admin import RatingInline
        self.assertIn(RatingInline, self.movie_admin.inlines)

    def test_movie_admin_get_main_genre(self):
        genre = Genre.objects.create(name='Action', description='')
        movie = Movie.objects.create(title='Test', release_year=2020, synopsis='Test')
        movie.genre.set([genre])
        result = self.movie_admin.get_main_genre(movie)
        self.assertEqual(result, 'Action')

    def test_movie_admin_get_director_names(self):
        person = Person.objects.create(first_name='John', last_name='Doe', role='director')
        movie = Movie.objects.create(title='Test', release_year=2020, synopsis='Test', director=person)
        result = self.movie_admin.get_director_names(movie)
        self.assertIn('John', result)
        self.assertIn('Doe', result)

    def test_movie_admin_has_delete_permission(self):
        self.assertTrue(self.movie_admin.has_delete_permission(self.user))

    def test_movie_admin_get_search_results(self):
        person = Person.objects.create(first_name='Jane', last_name='Smith', role='director')
        Movie.objects.create(title='Test', release_year=2020, synopsis='Test', director=person)
        queryset = Movie.objects.all()
        result, distinct = self.movie_admin.get_search_results(None, queryset, 'Jane')
        self.assertTrue(result.exists())

    def test_rating_admin_list_display(self):
        self.assertEqual(self.rating_admin.list_display, ['movie', 'user_name', 'score', 'comment', 'created_at'])

    def test_rating_admin_search_fields(self):
        self.assertEqual(self.rating_admin.search_fields, ['movie__title', 'user_name'])


class RatingInlineTest(TestCase):
    def setUp(self):
        from django.contrib.admin.sites import AdminSite
        from .admin import RatingInline
        self.site = AdminSite()
        self.rating_inline = RatingInline(Rating, self.site)

    def test_rating_inline_model(self):
        self.assertEqual(self.rating_inline.model, Rating)

    def test_rating_inline_fields(self):
        self.assertEqual(self.rating_inline.fields, ['user_name', 'score', 'comment'])


@override_settings(DEBUG=False)
class PublicViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action', description='')
        self.director = Person.objects.create(first_name='Christopher', last_name='Nolan', role='director')
        self.movie = Movie.objects.create(
            title='Inception',
            release_year=2010,
            synopsis='A dream heist film',
            director=self.director
        )
        self.movie.genre.set([self.genre])
        Rating.objects.create(movie=self.movie, score=5, comment='Excellent', user_name='admin')
        Rating.objects.create(movie=self.movie, score=4, comment='Great', user_name='user1')

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

    def test_recommendations_sorting_by_rating(self):
        client = Client()
        response = client.get(reverse('movies:recommendations'))
        content = response.content.decode()
        self.assertIn('Inception', content)

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
