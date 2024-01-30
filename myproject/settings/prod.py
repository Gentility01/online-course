from .base import *
import os

import dj_database_url
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"


 
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "online-course-7du1.onrender.com"]


DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
