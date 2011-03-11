import sys
import os

TOP_DIR = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
LIB_DIR = os.path.join(TOP_DIR, 'lib')
for p in (LIB_DIR, TOP_DIR):
    if p not in sys.path:
        sys.path.insert(0,p)

activate_this = os.path.join(ENV_DIR, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from django.core.management import execute_manager
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

