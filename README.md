# Lab05: Administrador en Django

## Descripción del Proyecto

Proyecto del **Laboratorio 05** del curso de **Desarrollo de Aplicaciones Empresariales**. Implementa un sistema de gestión de películas con Django Admin personalizado, incluyendo modelos, inlines, permisos por grupo, y una vista pública de recomendaciones con temática de streaming.

## Tecnologías Utilizadas

- **Python 3.12+**
- **Django 4.2.16**
- **MySQL** (MariaDB via XAMPP)
- **PyMySQL** como driver MySQL
- **Pillow** para soporte de imágenes
- **VS Code / OpenCode** como IDE
- **Git / GitHub** para control de versiones

## Estructura del Proyecto

```
lab05/
├── lab05/                  # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── movies/                 # Aplicación principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── seed_data.py
│   │       └── create_permissions.py
│   ├── templates/
│   │   └── movies/
│   │       └── recommendations.html
│   └── migrations/
│       └── 0001_initial.py
├── templates/              # Templates globales
├── static/                 # Archivos estáticos
├── media/                  # Medios subidos (covers)
├── requirements.txt
├── .gitignore
└── manage.py
```

## Modelos

### Genre
- `name` (CharField)
- `description` (TextField)
- `created_at`, `updated_at` (DateTimeField)

### Person
- `first_name`, `last_name` (CharField)
- `role` (ChoiceField: Director/Actor)
- `created_at`, `updated_at` (DateTimeField)

### Movie
- `title`, `release_year`, `synopsis` (CharField/IntegerField/TextField)
- `cover_image` (ImageField)
- `genre` (ManyToManyField a Genre)
- `director` (ForeignKey a Person)
- `created_at`, `updated_at` (DateTimeField)

### Rating
- `movie` (ForeignKey a Movie)
- `score` (IntegerField 1-5)
- `comment`, `user_name` (TextField/CharField)
- `created_at`, `updated_at` (DateTimeField)

## Comandos de Gestión

### Poblar la base de datos
```bash
python manage.py seed_data
```
Crea 4 géneros, 10 películas y 8 valoraciones.

### Crear permisos y usuarios
```bash
python manage.py create_permissions
```
Crea:
- Grupo `editores` con permisos de ADD y CHANGE en películas (sin DELETE)
- Usuario `editor_user` asignado al grupo `editores`
- Superusuario `admin` (usuario: `admin`, contraseña: `admin_password`)

## Configuración de Base de Datos

- **Motor**: MySQL (MariaDB)
- **Host**: 127.0.0.1
- **Puerto**: 3306
- **Base de datos**: `db_lab05_movies`
- **Usuario**: `root`
- **Contraseña**: (vacía)

Requiere XAMPP con MariaDB corriendo y la base de datos creada.

## Configuración del Administrador

El panel de administración (`/admin/`) incluye:

- **MovieAdmin**: `list_display`, `list_filter`, `search_fields`, `readonly_fields` y `RatingInline` (TabularInline)
- **GenreAdmin**, **PersonAdmin**, **RatingAdmin**: list_display y search_fields configurados

## Vista Pública

Accede a las recomendaciones en: `http://127.0.0.1:8000/recommendations/`

Presenta las películas mejor valoradas organizadas por género con un diseño de **Dark Mode** estilo plataforma de streaming (colores rojo `#E50914`, negro `#111111` y blanco `#FFFFFF`).

## Instalación y Ejecución

1. **Prerrequisitos**: Python 3.12+, XAMPP con MariaDB activo
2. Clonar el repositorio:
   ```bash
   git clone https://github.com/Johan-Salazar-Atencio/lab05_App_Empresariales.git
   cd lab05_App_Empresariales
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crear la base de datos MySQL:
   ```sql
   CREATE DATABASE db_lab05_movies CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```
6. Poblar datos:
   ```bash
   python manage.py seed_data
   python manage.py create_permissions
   ```
7. Ejecutar el servidor:
   ```bash
   python manage.py runserver
   ```
8. Acceder a:
   - Admin: `http://127.0.0.1:8000/admin/`
   - Recomendaciones: `http://127.0.0.1:8000/recommendations/`

## Notas del Laboratorio

- Los archivos de medios (covers) se almacenan en `media/covers/`
- El `settings.py` incluye configuración para servir archivos multimedia en desarrollo
- Los permisos del grupo `editores` están configurados para que solo puedan añadir y modificar películas, no eliminarlas
- El código sigue el estándar PEP 8 con nombres y comentarios en inglés, e interfaz pública en español
