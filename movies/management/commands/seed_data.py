from django.core.management.base import BaseCommand
from movies.models import Genre, Movie, Recommendation


class Command(BaseCommand):
    help = 'Seed the database with initial genres, movies, and recommendations'

    def handle(self, *args, **kwargs):
        self.seed_genres()
        self.seed_movies()
        self.seed_recommendations()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def seed_genres(self):
        genres_data = [
            'Action',
            'Science Fiction',
            'Drama',
            'Thriller',
        ]
        for name in genres_data:
            genre, created = Genre.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f'Created genre: {genre.name}')

    def seed_movies(self):
        genres = {g.name: g for g in Genre.objects.all()}

        movies_data = [
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through dream-sharing technology is given the task of planting an idea.',
                'release_year': 2010,
                'duration_minutes': 148,
                'genre': 'Action',
                'rating': 4.8,
            },
            {
                'title': 'Interstellar',
                'description': 'A team of explorers travel through a wormhole in space to ensure humanity\'s survival.',
                'release_year': 2014,
                'duration_minutes': 169,
                'genre': 'Science Fiction',
                'rating': 4.9,
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological and physical tests.',
                'release_year': 2008,
                'duration_minutes': 152,
                'genre': 'Action',
                'rating': 4.9,
            },
            {
                'title': 'Gravity',
                'description': 'Two astronauts are stranded in space after their shuttle is destroyed.',
                'release_year': 2013,
                'duration_minutes': 91,
                'genre': 'Science Fiction',
                'rating': 4.4,
            },
            {
                'title': 'Arrival',
                'description': 'A linguist works with the military to communicate with alien lifeforms.',
                'release_year': 2016,
                'duration_minutes': 116,
                'genre': 'Science Fiction',
                'rating': 4.5,
            },
            {
                'title': 'A Star Is Born',
                'description': 'A musician helps a young singer find fame as their relationship deteriorates.',
                'release_year': 2018,
                'duration_minutes': 136,
                'genre': 'Drama',
                'rating': 4.2,
            },
            {
                'title': 'Blade Runner 2049',
                'description': 'A young blade runner\'s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.',
                'release_year': 2017,
                'duration_minutes': 164,
                'genre': 'Science Fiction',
                'rating': 4.6,
            },
            {
                'title': 'The Martian',
                'description': 'An astronaut is stranded on Mars and must find a way to survive.',
                'release_year': 2015,
                'duration_minutes': 144,
                'genre': 'Science Fiction',
                'rating': 4.7,
            },
            {
                'title': 'Shutter Island',
                'description': 'A U.S. Marshal investigates a disappearance at a mental facility.',
                'release_year': 2010,
                'duration_minutes': 138,
                'genre': 'Thriller',
                'rating': 4.3,
            },
            {
                'title': '1917',
                'description': 'Two British soldiers must cross No Man\'s Land and deliver a message to save 1,600 lives.',
                'release_year': 2019,
                'duration_minutes': 119,
                'genre': 'Action',
                'rating': 4.5,
            },
        ]
        for data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'release_year': data['release_year'],
                    'duration_minutes': data['duration_minutes'],
                    'genre': genres[data['genre']],
                    'rating': data['rating'],
                }
            )
            if created:
                self.stdout.write(f'Created movie: {movie.title}')

    def seed_recommendations(self):
        recommendations_data = [
            {'movie_title': 'Inception', 'user': 'admin', 'score': 5, 'comment': 'Masterpiece of cinema'},
            {'movie_title': 'Inception', 'user': 'editor_user', 'score': 4, 'comment': 'Great plot and visuals'},
            {'movie_title': 'Interstellar', 'user': 'admin', 'score': 5, 'comment': 'Emotionally powerful'},
            {'movie_title': 'The Dark Knight', 'user': 'editor_user', 'score': 5, 'comment': 'Best superhero movie ever'},
            {'movie_title': 'Gravity', 'user': 'admin', 'score': 4, 'comment': 'Visual effects are stunning'},
            {'movie_title': 'Arrival', 'user': 'editor_user', 'score': 4, 'comment': 'Intelligent sci-fi'},
            {'movie_title': 'Blade Runner 2049', 'user': 'admin', 'score': 5, 'comment': 'Visually breathtaking'},
            {'movie_title': '1917', 'user': 'editor_user', 'score': 5, 'comment': 'Incredible one-shot experience'},
        ]
        for data in recommendations_data:
            movie = Movie.objects.get(title=data['movie_title'])
            rec, created = Recommendation.objects.get_or_create(
                movie=movie,
                user_name=data['user'],
                defaults={
                    'score': data['score'],
                    'comment': data['comment'],
                }
            )
            if created:
                self.stdout.write(f'Created recommendation: {rec}')
