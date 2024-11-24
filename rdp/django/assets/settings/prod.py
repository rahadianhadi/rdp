import os

from .base import *
from .env import *


DEBUG = False

ALLOWED_HOSTS = [v.strip() for v in os.getenv("ALLOWED_HOSTS", "").split(',') if v.strip()]

# Database settings
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE "),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

# Additional production-specific settings
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
