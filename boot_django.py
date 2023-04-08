# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.

import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "django_moncash"))

def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default":{
                "ENGINE":"django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            "django_moncash",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,

        MONCASH = {
            'CLIENT_ID':"e13daf9519d49a9e766f3718473575e4",
            'SECRET_KEY':"oHrr4tbnB1PH0uz6VQNUvSOO_KaiLSdH9uzX33EmgHarEuFWQdYztzwYnJ1IDASB",
            'ENVIRONMENT':"sandbox"
        }

    )
    django.setup()