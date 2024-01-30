from .base import *
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-9@2+)@hwiv(qk94oqf(9=@gcv)48k-il1t1h$a772e+e580#$y")



ALLOWED_HOSTS = ["127.0.0.1", "localhost", "online-course-prnw.onrender.com"]

if not DEBUG:
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }