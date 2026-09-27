# Configuración IntelliJ - Lab05 Django

## Paso 1: Configurar el intérprete de Python
1. File → Project Structure → SDKs
2. Añadir Python SDK → Seleccionar `C:\Users\Johan\AppData\Local\Programs\Python\Python314\python.exe`

## Paso 2: Habilitar soporte Django
1. File → Settings → Languages & Frameworks → Django
2. Marcar "Enable Django Support"
3. Django project root: `C:\App_Empresariales\Lab05`
4. Settings: `lab05.settings`
5. Manage script: `manage.py`

## Paso 3: Crear configuración de ejecución
1. Run → Edit Configurations → + → Django server
2. Name: `Lab05`
3. Host: `127.0.0.1` / Port: `8000`
4. Environment variables: `DJANGO_SETTINGS_MODULE=lab05.settings`
5. Python interpreter: seleccionar el configurado en Paso 1

## Paso 4: Sincronizar dependencias
1. Click derecho en `requirements.txt` → "Add as requirements file"
2. O: File → Settings → Project → Python Interpreter → Install from requirements.txt

## Paso 5: Ejecutar
- Click en el icono Play (▶) o Shift+F10
