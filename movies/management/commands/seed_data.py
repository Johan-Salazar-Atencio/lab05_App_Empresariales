from django.core.management.base import BaseCommand
from movies.models import Genre, Movie, Recommendation


class Command(BaseCommand):
    help = 'Seed the database with initial genres, movies, and recommendations in Spanish'

    def handle(self, *args, **kwargs):
        self.seed_genres()
        self.seed_movies()
        self.seed_recommendations()
        self.stdout.write(self.style.SUCCESS('Base de datos poblada con exito!'))

    def seed_genres(self):
        genre_mapping = {
            'Action': 'Accion',
            'Science Fiction': 'Ciencia Ficcion',
            'Drama': 'Drama',
            'Thriller': 'Suspenso',
        }
        for old_name, new_name in genre_mapping.items():
            genre, created = Genre.objects.get_or_create(name=old_name)
            if genre.name != new_name:
                genre.name = new_name
                genre.save()
                self.stdout.write(f'Genero actualizado: {old_name} -> {new_name}')
            elif created:
                self.stdout.write(f'Genero creado: {new_name}')

    def seed_movies(self):
        movies_data = [
            {
                'title': 'El Origen',
                'description': 'Un ladron que roba secretos corporativos a traves de la tecnologia de compartir sueños recibe la tarea de plantar una idea en la mente de un CEO.',
                'release_year': 2010,
                'duration_minutes': 148,
                'genre': 'Accion',
                'rating': 4.8,
            },
            {
                'title': 'Interstellar',
                'description': 'Un equipo de exploradores viaja a traves de un agujero de gusano en el espacio para garantizar la supervivencia de la humanidad.',
                'release_year': 2014,
                'duration_minutes': 169,
                'genre': 'Ciencia Ficcion',
                'rating': 4.9,
            },
            {
                'title': 'El Caballero de la Noche',
                'description': 'Cuando el Joker caos en Gotham, Batman debe aceptar una de las mayores pruebas psicologicas y fisicas de su capacidad para luchar contra la injusticia.',
                'release_year': 2008,
                'duration_minutes': 152,
                'genre': 'Accion',
                'rating': 4.9,
            },
            {
                'title': 'Gravedad',
                'description': 'Dos astronautas quedan varados en el espacio despues de que su transbordador sea destruido y deben encontrar una manera de volver a la Tierra.',
                'release_year': 2013,
                'duration_minutes': 91,
                'genre': 'Ciencia Ficcion',
                'rating': 4.4,
            },
            {
                'title': 'La Llegada',
                'description': 'Una linguista trabaja con el ejercito para comunicarse con formas de vida alienigenas que han llegado a la Tierra.',
                'release_year': 2016,
                'duration_minutes': 116,
                'genre': 'Ciencia Ficcion',
                'rating': 4.5,
            },
            {
                'title': 'Nace una Estrella',
                'description': 'Un musico ayuda a una joven cantante a encontrar la fama mientras su propia carrera se desmorona debido a problemas personales.',
                'release_year': 2018,
                'duration_minutes': 136,
                'genre': 'Drama',
                'rating': 4.2,
            },
            {
                'title': 'Blade Runner 2049',
                'description': 'El descubrimiento de un secreto largamente enterrado lleva a un nuevo blade runner a buscar al ex blade runner Rick Deckard.',
                'release_year': 2017,
                'duration_minutes': 164,
                'genre': 'Ciencia Ficcion',
                'rating': 4.6,
            },
            {
                'title': 'Mision Rescate',
                'description': 'Un astronauta queda varado en Marte y debe encontrar una manera de sobrevivir mientras el equipo en la Tierra intenta rescatarlo.',
                'release_year': 2015,
                'duration_minutes': 144,
                'genre': 'Ciencia Ficcion',
                'rating': 4.7,
            },
            {
                'title': 'La Isla Siniestra',
                'description': 'Un alguacil de los Estados Unidos investiga la desaparicion de una paciente en un hospital psiquiatrico ubicado en una isla remota.',
                'release_year': 2010,
                'duration_minutes': 138,
                'genre': 'Suspenso',
                'rating': 4.3,
            },
            {
                'title': '1917',
                'description': 'Dos soldados britanicos deben cruzar la tierra de nadie y entregar un mensaje para salvar a 1.600 vidas durante la Primera Guerra Mundial.',
                'release_year': 2019,
                'duration_minutes': 119,
                'genre': 'Accion',
                'rating': 4.5,
            },
        ]

        title_mapping = {
            'Inception': 'El Origen',
            'Interstellar': 'Interstellar',
            'The Dark Knight': 'El Caballero de la Noche',
            'Gravity': 'Gravedad',
            'Arrival': 'La Llegada',
            'A Star Is Born': 'Nace una Estrella',
            'Blade Runner 2049': 'Blade Runner 2049',
            'The Martian': 'Mision Rescate',
            'Shutter Island': 'La Isla Siniestra',
            '1917': '1917',
        }

        for data in movies_data:
            old_title = None
            for eng, spa in title_mapping.items():
                if data['title'] == spa:
                    old_title = eng
                    break

            movie = Movie.objects.filter(title=data['title']).first()
            if not movie and old_title:
                movie = Movie.objects.filter(title=old_title).first()

            if movie:
                movie.title = data['title']
                movie.description = data['description']
                movie.release_year = data['release_year']
                movie.duration_minutes = data['duration_minutes']
                movie.rating = data['rating']
                genre = Genre.objects.get(name=data['genre'])
                movie.genre = genre
                movie.save()
                self.stdout.write(f'Pelicula actualizada: {movie.title}')
            else:
                genre = Genre.objects.get(name=data['genre'])
                movie = Movie.objects.create(
                    title=data['title'],
                    description=data['description'],
                    release_year=data['release_year'],
                    duration_minutes=data['duration_minutes'],
                    genre=genre,
                    rating=data['rating'],
                )
                self.stdout.write(f'Pelicula creada: {movie.title}')

    def seed_recommendations(self):
        recommendations_data = [
            {'movie_title': 'El Origen', 'user': 'admin', 'score': 5, 'comment': 'Obra maestra del cine'},
            {'movie_title': 'El Origen', 'user': 'editor_user', 'score': 4, 'comment': 'Gran trama y efectos visuales'},
            {'movie_title': 'Interstellar', 'user': 'admin', 'score': 5, 'comment': 'Emotivamente poderosa'},
            {'movie_title': 'El Caballero de la Noche', 'user': 'editor_user', 'score': 5, 'comment': 'La mejor pelicula de superheroes'},
            {'movie_title': 'Gravedad', 'user': 'admin', 'score': 4, 'comment': 'Efectos visuales impresionantes'},
            {'movie_title': 'La Llegada', 'user': 'editor_user', 'score': 4, 'comment': 'Ciencia ficcion inteligente'},
            {'movie_title': 'Blade Runner 2049', 'user': 'admin', 'score': 5, 'comment': 'Visualmente impresionante'},
            {'movie_title': '1917', 'user': 'editor_user', 'score': 5, 'comment': 'Experiencia de plano secuencia increible'},
        ]

        for data in recommendations_data:
            movie = Movie.objects.filter(title=data['movie_title']).first()
            if not movie:
                for eng, spa in {
                    'Inception': 'El Origen',
                    'The Dark Knight': 'El Caballero de la Noche',
                    'Gravity': 'Gravedad',
                    'Arrival': 'La Llegada',
                }.items():
                    if data['movie_title'] == spa:
                        movie = Movie.objects.filter(title=eng).first()
                        break

            if movie:
                rec, created = Recommendation.objects.get_or_create(
                    movie=movie,
                    user_name=data['user'],
                    defaults={
                        'score': data['score'],
                        'comment': data['comment'],
                    }
                )
                if created:
                    self.stdout.write(f'Recomendacion creada: {rec}')
