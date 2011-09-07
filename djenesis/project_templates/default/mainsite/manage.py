#!/usr/bin/env python
import sys
import os

# Path to the whole project (one level up from mainsite)
TOP_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# Apps written for the project go in this directory
APPS_DIR = os.path.join(TOP_DIR, "apps")

for p in (APPS_DIR, TOP_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)


from django.core.management import execute_manager

try:
    import settings  # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
