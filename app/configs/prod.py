from .base import *
from decouple import config

# import dj_database_url

DEBUG = config("DEBUG")
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS").split(",")
# print(CSRF_TRUSTED_ORIGINS)


DATABASES = {
    # "default": dj_database_url.parse(config("DB_URL")),
}
