from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-homework-key-change-before-deployment"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "tasks.middleware.HttpRequestLoggingMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangohomework8.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangohomework8.wsgi.application"
ASGI_APPLICATION = "djangohomework8.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Глобальная пагинация для списков API.
# Логи сохраняются в папке logs в корне проекта.
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {name}: {message}",
            "style": "{",
        },
        "http": {
            "format": "{asctime} {levelname}: {message}",
            "style": "{",
        },
        "database": {
            "format": "{asctime} {levelname}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        # Логи запущенного Django-сервера остаются в консоли.
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
        # HTTP-запросы и статусы ответов записываются отдельно.
        "http_file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "http_logs.log",
            "formatter": "http",
            "level": "INFO",
            "encoding": "utf-8",
        },
        # SQL-запросы Django записываются отдельно.
        "db_file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "db_logs.log",
            "formatter": "database",
            "level": "DEBUG",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "project.http": {
            "handlers": ["http_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["db_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


# JWT-аутентификация, права доступа и глобальная пагинация.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    # Читать API можно без входа, но создавать, менять и удалять —
    # только после получения JWT-токена.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "tasks.pagination.SafeCursorPagination",
    "PAGE_SIZE": 5,
}
