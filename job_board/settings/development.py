from .base import *

INSTALLED_APPS += [
    "silk",
    "drf_spectacular",
    "django_extensions",
]
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Allow React frontend running locally
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEBUG = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
