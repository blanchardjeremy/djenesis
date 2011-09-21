import sys
import os
from django.core.handlers.wsgi import WSGIHandler

# assume that we are in a directory that is direct descendant of top_dir, e.g.: TOP_DIR/etc/start.wsgi
TOP_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# assume that the virtualenv is a directory named 'env' sibling to TOP_DIR
ENV_DIR = os.path.join(os.path.dirname(TOP_DIR), 'env')

sys.path.insert(0,TOP_DIR)

# if virtualenv exists, actiavte it
activate_this = os.path.join(ENV_DIR, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    execfile(activate_this, dict(__file__=activate_this))

# call through to the django application
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite.settings'
application = WSGIHandler()

