import os
from .base import (
    BASE_DIR, SECRET_KEY, INSTALLED_APPS, MIDDLEWARE 
  )


#---------------------------------------------------
# Settings
SECRET_KEY = os.getenv('SECRET_KEY', default='')

INSTALLED_APPS += [v.strip() for v in os.getenv('LIBS', default='').split(',') if v.strip()]
INSTALLED_APPS += [v.strip() for v in os.getenv('LIBS_FE', default='').split(',') if v.strip()]
INSTALLED_APPS += [v.strip() for v in os.getenv('LIBS_API', default='').split(',') if v.strip()]

INSTALLED_APPS += [v.strip() for v in os.getenv('APPS', default='').split(',') if v.strip()]

MIDDLEWARE += [v.strip() for v in os.getenv('MIDDLEWARE', default='').split(',') if v.strip()]

# Static
# Folder untuk file statis asli (misalnya CSS, JS, dan gambar)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Menyimpan file statis yang digunakan di dev (misalnya style.css)
]

# Folder tempat Django akan mengumpulkan semua file statis untuk produksi (collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Tempat hasil collectstatic akan disalin

# Menyediakan lokasi untuk file-file yang digunakan secara dinamis, seperti di S3 (jika diperlukan)
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# ---------------------------------------------------
# Django Cotton
COTTON_DIR = BASE_DIR / "templates/components"


# ---------------------------------------------------
# Django Rest-framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    
    # Control the rate of requests using DRF’s throttling mechanism.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/day',
    }
}

#
# Cache
# @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }
