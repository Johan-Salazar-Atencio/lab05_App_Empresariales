from django.core.management.base import BaseCommand
from movies.models import Genre, Person, Movie, Rating


class Command(BaseCommand):
    help = 'Seed the database with initial genres, movies, people, and ratings'

    def handle(self, *args, **kwargs):
        self.seed_genres()
        self.seed_people()
        self.seed_movies()
        self.seed_ratings()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def seed_genres(self):
        genres_data = [
            {'name': 'Action', 'description': 'High-energy films with intense sequences'},
            {'name': 'Science Fiction', 'description': 'Futuristic stories exploring technology and space'},
            {'name': 'Drama', 'description': 'Emotionally intense character-driven stories'},
            {'name': 'Thriller', 'description': 'Suspenseful and psychological tension-filled narratives'},
        ]
        for data in genres_data:
            genre, created = Genre.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                self.stdout.write(f'Created genre: {genre.name}')

    def seed_people(self):
        people_data = [
            {'first_name': 'Christopher', 'last_name': 'Nolan', 'role': 'director'},
            {'first_name': 'Alfonso', 'last_name': 'Cuaron', 'role': 'director'},
            {'first_name': 'Denis', 'last_name': 'Villeneuve', 'role': 'director'},
            {'first_name': 'Bradley', 'last_name': 'Cooper', 'role': 'actor'},
            {'first_name': 'Sandra', 'last_name': 'Bullock', 'role': 'actor'},
            {'first_name': 'Matt', 'last_name': 'Damon', 'role': 'actor'},
            {'first_name': 'Leonardo', 'last_name': 'DiCaprio', 'role': 'actor'},
            {'first_name': 'Scarlett', 'last_name': 'Johansson', 'role': 'actor'},
            {'first_name': 'Harrison', 'last_name': 'Ford', 'role': 'actor'},
            {'first_name': 'Emma', 'last_name': 'Stone', 'role': 'actor'},
        ]
        for data in people_data:
            person, created = Person.objects.get_or_create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created person: {person}')

    def seed_movies(self):
        genre_names = ['Action', 'Science Fiction', 'Drama', 'Thriller']
        genres = {g.name: g for g in Genre.objects.all()}
        people = {
            'nolan': Person.objects.get(first_name='Christopher', last_name='Nolan'),
            'cuaron': Person.objects.get(first_name='Alfonso', last_name='Cuaron'),
            'villeneuve': Person.objects.get(first_name='Denis', last_name='Villeneuve'),
            'cooper': Person.objects.get(first_name='Bradley', last_name='Cooper'),
            'bullock': Person.objects.get(first_name='Sandra', last_name='Bullock'),
            'damon': Person.objects.get(first_name='Matt', last_name='Damon'),
            'diCaprio': Person.objects.get(first_name='Leonardo', last_name='DiCaprio'),
            'johansson': Person.objects.get(first_name='Scarlett', last_name='Johansson'),
            'ford': Person.objects.get(first_name='Harrison', last_name='Ford'),
            'stone': Person.objects.get(first_name='Emma', last_name='Stone'),
        }

        movies_data = [
            {
                'title': 'Interstellar', 'release_year': 2014,
                'synopsis': 'A team of explorers travel through a wormhole in space to ensure humanity\'s survival.',
                'genres': ['Science Fiction', 'Drama'], 'director': 'nolan',
            },
            {
                'title': 'Gravity', 'release_year': 2013,
                'synopsis': 'Two astronauts are stranded in space after their shuttle is destroyed.',
                'genres': ['Science Fiction', 'Thriller'], 'director': 'cuaron',
            },
            {
                'title': 'Arrival', 'release_year': 2016,
                'synopsis': 'A linguist works with the military to communicate with alien lifeforms.',
                'genres': ['Science Fiction', 'Drama'], 'director': 'villeneuve',
            },
            {
                'title': 'The Dark Knight', 'release_year': 2008,
                'synopsis': 'When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological and physical tests.',
                'genres': ['Action', 'Thriller'], 'director': 'nolan',
            },
            {
                'title': 'A Star Is Born', 'release_year': 2018,
                'synopsis': 'A musician helps a young singer find fame as their relationship deteriorates.',
                'genres': ['Drama', 'Action'], 'director': 'cooper',
            },
            {
                'title': 'Blade Runner 2049', 'release_year': 2017,
                'synopsis': 'A young blade runner\'s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.',
                'genres': ['Science Fiction', 'Thriller'], 'director': 'villeneuve',
            },
            {
                'title': 'The Martian', 'release_year': 2015,
                'synopsis': 'An astronaut is stranded on Mars and must find a way to survive.',
                'genres': ['Science Fiction', 'Drama'], 'director': 'damon',
            },
            {
                'title': 'Shutter Island', 'release_year': 2010,
                'synopsis': 'A U.S. Marshal investigates a disappearance at a mental facility.',
                'genres': ['Thriller'], 'director': 'diCaprio',
            },
            {
                'title': '1917', 'release_year': 2019,
                'synopsis': 'Two British soldiers must cross No Man\'s Land and deliver a message to save 1,600 lives.',
                'genres': ['Action', 'Drama', 'Thriller'], 'director': 'cuaron',
            },
            {
                'title': 'Inception', 'release_year': 2010,
                'synopsis': 'A thief who steals corporate secrets through dream-sharing technology is given a task to plant an idea.',
                'genres': ['Action', 'Science Fiction', 'Thriller'], 'director': 'nolan',
            },
        ]
        for data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                defaults={
                    'release_year': data['release_year'],
                    'synopsis': data['synopsis'],
                    'director': people[data['director']],
                }
            )
            if created:
                movie.genre.set(genres[g] for g in data['genres'])
                self.stdout.write(f'Created movie: {movie.title}')
            else:
                movie.genre.set(genres[g] for g in data['genres'])
                movie.director = people[data['director']]
                movie.save()

    def seed_ratings(self):
        movies = list(Movie.objects.all())
        ratings_data = [
            {'movie_title': 'Inception', 'user': 'admin', 'score': 5, 'comment': 'Masterpiece of cinema'},
            {'movie_title': 'Inception', 'user': 'editor_user', 'score': 4, 'comment': 'Great plot'},
            {'movie_title': 'Interstellar', 'user': 'admin', 'score': 5, 'comment': 'Emotionally powerful'},
            {'movie_title': 'The Dark Knight', 'user': 'editor_user', 'score': 5, 'comment': 'Best superhero movie ever'},
            {'movie_title': 'Gravity', 'user': 'admin', 'score': 4, 'comment': 'Visual effects are stunning'},
            {'movie_title': 'Arrival', 'user': 'editor_user', 'score': 4, 'comment': 'Intelligent sci-fi'},
            {'movie_title': 'Blade Runner 2049', 'user': 'admin', 'score': 5, 'comment': 'Visually breathtaking'},
            {'movie_title': '1917', 'user': 'editor_user', 'score': 5, 'comment': 'Incredible one-shot experience'},
        ]
        for data in ratings_data:
            movie = Movie.objects.get(title=data['movie_title'])
            rating, created = Rating.objects.get_or_create(
                movie=movie,
                user_name=data['user'],
                defaults={
                    'score': data['score'],
                    'comment': data['comment'],
                }
            )
            if created:
                self.stdout.write(f'Created rating: {rating}')
