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
SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}
DEBUG = True
