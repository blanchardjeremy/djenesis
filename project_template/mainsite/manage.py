#!/usr/bin/env python
import sys
from os import path


PROJECT_DIR = path.abspath(path.dirname(__file__).decode('utf-8'))
TOP_DIR = path.abspath(path.dirname(PROJECT_DIR).decode('utf-8'))
LIB_DIR = path.join(TOP_DIR,"lib")
APP_DIR = path.join(TOP_DIR,"apps")

# Include the PROJECT_DIR and TOP_DIR in the python path.
for p in (PROJECT_DIR, TOP_DIR, LIB_DIR, APP_DIR):
    if p not in sys.path:
        sys.path.insert(0,p)

from django.core.management import execute_manager

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)