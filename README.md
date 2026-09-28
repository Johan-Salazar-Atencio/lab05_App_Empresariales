# Lab 05 - Aplicacion de Peliculas en Django

## Descripcion del Proyecto

Aplicacion web de catalogo de peliculas desarrollada con Django como parte del Laboratorio 05 del curso de Desarrollo de Aplicaciones Empresariales. Incluye un sistema completo de CRUD, panel de administracion personalizado, recomendaciones de usuarios y una interfaz dark mode estilo Netflix.

## Arquitectura de Datos

### Modelos

#### Genre
- `name` (CharField, unico) - Nombre del genero

#### Movie
- `title` (CharField) - Titulo de la pelicula
- `description` (TextField) - Sinopsis
- `release_year` (PositiveIntegerField) - Ano de estreno
- `duration_minutes` (PositiveIntegerField) - Duracion en minutos
- `poster` (ImageField) - Poster de la pelicula (opcional)
- `genre` (ForeignKey a Genre) - Genero principal
- `rating` (DecimalField) - Calificacion 0.0 - 5.0
- `created_at` / `updated_at` (DateTimeField) - Auditoria

#### Recommendation
- `movie` (ForeignKey a Movie) - Pelicula recomendada
- `user_name` (CharField) - Nombre del usuario
- `comment` (TextField) - Comentario
- `score` (PositiveIntegerField) - Puntuacion 1-5
- `created_at` (DateTimeField) - Fecha de creacion

### Relaciones

- `Genre` 1:N `Movie` (un genero tiene muchas peliculas)
- `Movie` 1:N `Recommendation` (una pelicula tiene muchas recomendaciones)

## Requisitos Previos

- Python 3.12+
- MySQL (XAMPP con MariaDB)
- pip

## Instalacion y Ejecucion

### 1. Crear base de datos

```sql
CREATE DATABASE db_lab05_movies CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Instalar dependencias

```bash
pip install django Pillow pymysql
```

### 3. Ajustar configuracion (lab05/settings.py)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_lab05_movies',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 4. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Poblar datos (opcional)

```bash
python manage.py seed_data
python manage.py create_permissions
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

### URLs

| URL | Descripcion |
|-----|-------------|
| `http://127.0.0.1:8000/` | Catalogo de peliculas |
| `http://127.0.0.1:8000/<id>/` | Detalle de pelicula |
| `http://127.0.0.1:8000/create/` | Agregar pelicula |
| `http://127.0.0.1:8000/<id>/update/` | Editar pelicula |
| `http://127.0.0.1:8000/<id>/delete/` | Eliminar pelicula |
| `http://127.0.0.1:8000/admin/` | Panel de administracion |

## Panel de Administracion

### Acceso
- Usuario: `admin` / Contrasena: `admin_password`
- Editor: `editor_user` / Contrasena: `editor_password`

### Permisos del grupo Editores
- Puede AGREGAR peliculas
- Puede EDITAR peliculas
- NO puede ELIMINAR peliculas

## Comandos de Gestión

| Comando | Descripcion |
|---------|-------------|
| `python manage.py seed_data` | Pobla la BD con datos de prueba |
| `python manage.py create_permissions` | Crea grupo y usuarios de prueba |
| `python manage.py runserver` | Inicia el servidor de desarrollo |

## Estructura del Proyecto

```
lab05/
├── lab05/              # Configuracion Django
├── movies/             # Aplicacion principal
│   ├── models.py       # Modelos Genre, Movie, Recommendation
│   ├── forms.py        # Formularios MovieForm, GenreForm, RecommendationForm
│   ├── views.py        # Vistas CRUD
│   ├── admin.py        # Configuracion del admin
│   ├── urls.py         # Rutas de la app
│   └── templates/      # Templates HTML
├── templates/          # Templates globales
├── static/             # Archivos estaticos
└── manage.py
```

## Capturas de Pantalla

### Catalogo
El catalogo muestra las peliculas organizadas por genero en un grid responsivo con busqueda y filtros.

### Detalle
Cada pelicula muestra su informacion completa y permite agregar recomendaciones.

### CRUD
Formularios en modo oscuro para agregar, editar y eliminar peliculas.
