import imp
import sys
import os


# Path to mainsite
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
# Path to the whole project (one level up from mainsite)
TOP_DIR = os.path.dirname(PROJECT_DIR)
# Required python libraries should go in this directory
LIB_DIR = os.path.join(TOP_DIR, "lib")
# Apps written for the project go in this directory
APP_DIR = os.path.join(TOP_DIR, "apps")

for p in (APP_DIR, LIB_DIR, TOP_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)



INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'south',
    'csky',

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
    'jingo.loaders.Loader',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
]
JINGO_EXCLUDE=['admin','debug_toolbar']




# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


# --- Generic configuration section ---
# This section will usually not need to be modified on a per-project basis.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(TOP_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

ROOT_URLCONF = 'mainsite.urls'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
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
