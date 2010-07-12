import sys
import os

TOP_DIR = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
LIB_DIR = os.path.join(TOP_DIR, 'lib')
PROJECT_DIR = os.path.join(TOP_DIR, 'mainsite')

# Include the PROJECT_DIR and TOP_DIR in the python path.
for p in (PROJECT_DIR, TOP_DIR, LIB_DIR):
    if p not in sys.path:
        sys.path.insert(0,p)

from django.core.management import execute_manager
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

