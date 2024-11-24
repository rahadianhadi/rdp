import os

from .base import *
from .env import *


DEBUG = True

# Database settings
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE"),
        "NAME": BASE_DIR / os.getenv("DATABASE_NAME"),
    }
}

