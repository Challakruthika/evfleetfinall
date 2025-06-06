import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Supabase Configuration
SUPABASE_URL = 'https://exeobxeodzxirzdgymcd.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV4ZW9ieGVvZHp4aXJ6ZGd5bWNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkyMzI4MTksImV4cCI6MjA2NDgwODgxOX0.V_vLv4xU_LzbKM7YWl2eOxP9QUfcMyyAL4YB31u9LPE'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Database Configuration for Supabase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': f'{SUPABASE_URL.replace("https://", "")}.postgres.supabase.co',
        'NAME': 'postgres',
        'USER': 'postgres.exeobxeodzxirzdgymcd',
        'PASSWORD': 'postgres',  # This will be overridden by environment variable
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

# Override database settings with environment variables if available
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4o18b$kexd8cn-_$a0hvvjmzyj17y3uob^64pr_akb%+^tp%c0')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'users',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_plotly_dash',
    'django_bootstrap5',  # Optional for styling
    'channels',  # Required for live updates
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.SupabaseAuthMiddleware',  # Add Supabase middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',  # For Plotly Dash
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',  # Optional
]

ROOT_URLCONF = "ev_fleet_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'users/templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ev_fleet_management.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# User model setting
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # URL to access static files

# Add this to point to the static directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ev_fleet_management/static'),  # Location of static files in the project
    os.path.join(BASE_DIR, 'users/static'),
]

# Add STATIC_ROOT for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ASGI_APPLICATION = 'ev_fleet_management.asgi.application'

# Redis Channel Layer Configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Login URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'fleet_manager_home'  # or 'driver_home' depending on user role

# Authentication settings
AUTHENTICATION_BACKENDS = [
    'users.auth_backend.SupabaseAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep default backend as fallback
]
