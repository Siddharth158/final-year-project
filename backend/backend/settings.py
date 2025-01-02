from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-0zf$2ohjx(ep8pez9)x&hru93phqg+7v&^rnmgqp_s!$*e%o6o"

DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 20485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20485760  # 10MB
# Application definition
CORS_ALLOWED_ORIGINS = [
    "https://2f7f-103-246-193-34.ngrok-free.app",
    "http://localhost:5173",
    "http://192.168.56.1:5173",
    "http://192.168.137.1:5173",
    "http://172.16.12.200:5173",
    "https://48c6-103-246-193-34.ngrok-free.app"  # Add this origin as well
]
CSRF_TRUSTED_ORIGINS = [
   "https://2f7f-103-246-193-34.ngrok-free.app",
      "http://localhost:5173",
  "http://192.168.56.1:5173",
  "http://192.168.137.1:5173",
"http://172.16.12.200:5173"
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "student",
    "rest_framework_simplejwt",
    "corsheaders",
    "teacher",
]
# AUTH_USER_MODEL = 'student.Student'


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'student.authentication.DebugJWTAuthentication', 
        'rest_framework_simplejwt.authentication.JWTAuthentication',# Handles JWT
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Enforces authentication globally
    ],
}

AUTHENTICATION_BACKENDS = [
    'student.backends.USNAuthBackend',
    'teacher.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

from datetime import timedelta
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
USE_L10N = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,  # Set to True if you want refresh tokens to rotate
    'BLACKLIST_AFTER_ROTATION': False,  # Set to True if using blacklisting
    'AUTH_HEADER_TYPES': ('Bearer',),  # Authorization header prefix
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

