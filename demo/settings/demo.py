"""
    This file configures a demo environment
"""
from .defaults import *

# using django dev server so we will need to serve the static files (see urls.py)
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.path.dirname(BASE_DIR), "db.sqlite3"),
    }
}
