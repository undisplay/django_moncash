#!/usr/bin/env python
# makemigrations.py

from django.core.management import call_command
from boot_django import boot_django



import sys


def main():

    boot_django()
    call_command("makemigrations")



if __name__ == "__main__":
    sys.exit(main())