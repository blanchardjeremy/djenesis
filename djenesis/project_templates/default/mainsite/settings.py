import imp
import sys
import os


# Path to the whole project (one level up from mainsite)
TOP_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# Apps written for the project go in this directory
APPS_DIR = os.path.join(TOP_DIR, "apps")

for p in (APPS_DIR, TOP_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)



INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'mainsite',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
]



USE_I18N = False




# --- Generic configuration section ---
# This section will usually not need to be modified on a per-project basis.

TIME_ZONE = None  #  use the systems time zone

SITE_ID = 1

MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

ROOT_URLCONF = 'mainsite.urls'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = [
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(TOP_DIR, 'templates'),
]




try:
    from mainsite import local_settings
    settings_dict = globals()

    #update the global settings with all uppercase values from local_settings
    settings_dict.update( dict(filter(lambda (k, v): k.isupper(), local_settings.__dict__.items())) )

    #call local_settings.setup with a dictionary of the final settings if present
    if hasattr(local_settings, 'setup') and callable(local_settings.setup):
        local_settings.setup(settings_dict)
except ImportError:
    pass
