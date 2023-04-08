#!/usr/bin/env python

from django.core.management import call_command

from boot_django import boot_django

# call the django setup routine

import sys

def main():
    boot_django()
    call_command("shell")

if __name__ == "__main__":
    sys.exit(main())