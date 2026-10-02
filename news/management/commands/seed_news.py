from django.core.management.base import BaseCommand
from news.models import Author, Category, Article
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed the news database with categories, authors, and articles'

    def handle(self, *args, **kwargs):
        self.seed_categories()
        self.seed_authors()
        self.seed_articles()
        self.stdout.write(self.style.SUCCESS('Datos de noticias cargados con exito!'))

    def seed_categories(self):
        categories_data = [
            {'name': 'Tecnologia', 'description': 'Noticias sobre tecnologia, gadgets y avances cientificos.'},
            {'name': 'Deportes', 'description': 'Resultados, analisis y noticias del mundo deportivo.'},
            {'name': 'Cultura', 'description': 'Arte, musica, cine, literatura y eventos culturales.'},
        ]
        for data in categories_data:
            cat, created = Category.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                self.stdout.write(f'Categoria creada: {cat.name}')

    def seed_authors(self):
        authors_data = [
            {
                'name': 'Maria Garcia',
                'bio': 'Periodista tecnologica con mas de 10 anos de experiencia cubriendo la industria del software y la inteligencia artificial.',
            },
            {
                'name': 'Carlos Rodriguez',
                'bio': 'Cronista deportivo y cultural, especializado en futbol internacional y eventos artisticos latinoamericanos.',
            },
        ]
        for data in authors_data:
            author, created = Author.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                self.stdout.write(f'Autor creado: {author.name}')

    def seed_articles(self):
        maria = Author.objects.get(name='Maria Garcia')
        carlos = Author.objects.get(name='Carlos Rodriguez')
        tech = Category.objects.get(name='Tecnologia')
        sports = Category.objects.get(name='Deportes')
        culture = Category.objects.get(name='Cultura')

        now = timezone.now()
        articles_data = [
            {
                'title': 'La Inteligencia Artificial revoluciona la medicina',
                'summary': 'Nuevos algoritmos de IA permiten diagnosticar enfermedades con mayor precision que los metodos tradicionales.',
                'body': 'Un equipo de investigadores ha desarrollado un sistema de inteligencia artificial capaz de detectar enfermedades en etapas tempranas con una precision del 95%. Este avance promete transformar la forma en que los medicos abordan el diagnostico y tratamiento de pacientes en todo el mundo.',
                'author': maria,
                'categories': [tech],
                'published_at': now - timedelta(days=1),
            },
            {
                'title': 'Nuevo smartphone con bateria de grafeno',
                'summary': 'Una empresa lanza al mercado el primer telefono con bateria de grafeno que carga en 10 minutos.',
                'body': 'La tecnologia de grafeno llega finalmente a los dispositivos moviles comerciales. Este nuevo smartphone ofrece una bateria que se carga completamente en solo 10 minutos y tiene una duracion de hasta 72 horas de uso continuo.',
                'author': maria,
                'categories': [tech],
                'published_at': now - timedelta(days=3),
            },
            {
                'title': 'Final de Champions: resultado y analisis',
                'summary': 'Resumen completo de la final de la Champions League con los mejores momentos del partido.',
                'body': 'La final de la Champions League vivio un partido lleno de emociones. El equipo local se impuso por 2-1 con un gol en el minuto 89 que definió el campeonato. Analizamos las tacticas, los jugadores clave y lo que significa este titulo para la historia del club.',
                'author': carlos,
                'categories': [sports],
                'published_at': now - timedelta(days=2),
            },
            {
                'title': 'El renacimiento del cine latinoamericano',
                'summary': 'Nuevas producciones de America Latina estan ganando reconocimiento en festivales internacionales.',
                'body': 'El cine latinoamericano vive una epoca dorada con peliculas que han sido premiadas en Cannes, Berlin y Venecia. Directores emergentes estan contando historias universales desde perspectivas unicas que resuenan con audiencias de todo el mundo.',
                'author': carlos,
                'categories': [culture],
                'published_at': now - timedelta(days=5),
            },
            {
                'title': 'Robots en el campo: el futuro del futbol',
                'summary': 'La tecnologia llega a los entrenamientos de futbol con robots que analizan el rendimiento de los jugadores.',
                'body': 'Los clubes de futbol mas importantes del mundo estan incorporando robots y sensores en sus entrenamientos para analizar el rendimiento de los jugadores en tiempo real. Esta tecnologia permite optimizar tacticas y prevenir lesiones.',
                'author': maria,
                'categories': [tech, sports],
                'published_at': now - timedelta(days=7),
            },
            {
                'title': 'Festival de Musica 2026: cartel confirmado',
                'summary': 'Se revela el cartel completo del festival de musica mas importante del ano con artistas internacionales.',
                'body': 'El Festival de Musica 2026 anuncia su cartel con mas de 50 artistas de 15 paises diferentes. El evento se llevara a cabo durante tres dias y espera recibir a mas de 100,000 asistentes con una variedad de generos musicales.',
                'author': carlos,
                'categories': [culture],
                'published_at': now - timedelta(days=10),
            },
        ]

        for data in articles_data:
            article, created = Article.objects.get_or_create(
                title=data['title'],
                defaults={
                    'summary': data['summary'],
                    'body': data['body'],
                    'author': data['author'],
                    'published_at': data['published_at'],
                }
            )
            if created:
                article.categories.set(data['categories'])
                self.stdout.write(f'Articulo creado: {article.title}')
