from .settings import *

# Sobrescribir configuraciones sensibles mediante variables de entorno
import os

# Cargar .env si existe (útil en despliegues o en entornos locales)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, '.env'))
except Exception:
    # python-dotenv no está instalado o no se pudo cargar; seguimos con las variables de entorno del sistema
    pass

# SECRET_KEY: mantener el existente si no se proporciona por variable de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# DEBUG desde variable de entorno (valor por defecto: False en producción)
DEBUG = os.environ.get('DEBUG', str(DEBUG)).lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS desde variable de entorno (coma-separados)
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS').split(',') if h.strip()]

# Configuración de base de datos: usar DATABASE_URL si está presente
try:
    import dj_database_url
except Exception:
    dj_database_url = None

if os.environ.get('DATABASE_URL') and dj_database_url:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
# si no hay DATABASE_URL, dejamos la configuración de DATABASES que ya vino desde settings.py

# Static files (WhiteNoise)
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

# Insertar WhiteNoise en MIDDLEWARE justo después de SecurityMiddleware si no está presente
try:
    middleware = list(MIDDLEWARE)
except NameError:
    middleware = []

whitenoise_path = 'whitenoise.middleware.WhiteNoiseMiddleware'
if whitenoise_path not in middleware:
    if 'django.middleware.security.SecurityMiddleware' in middleware:
        idx = middleware.index('django.middleware.security.SecurityMiddleware') + 1
        middleware.insert(idx, whitenoise_path)
    else:
        middleware.insert(0, whitenoise_path)

MIDDLEWARE = middleware

# Opciones de seguridad recomendadas
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')

# Habilitar compresión y caching de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
