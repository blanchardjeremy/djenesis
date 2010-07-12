# Django settings for {{ project_name }} project.
import imp
import sys
from os import path

# Path to the django project (mainsite)
PROJECT_DIR = path.abspath(path.dirname(__file__).decode('utf-8'))
# Path to the whole project (one level up from mainsite)
TOP_DIR = path.abspath(path.dirname(PROJECT_DIR).decode('utf-8'))
# Required python libraries should go in this directory 
LIB_DIR = path.join(TOP_DIR,"lib")
# Apps written for the project go in this directory
APP_DIR = path.join(TOP_DIR,"apps")
# Prepend the above directories to the python path
for p in (PROJECT_DIR, TOP_DIR, LIB_DIR, APP_DIR):
    if p not in sys.path:
        sys.path.insert(0,p)


# --- Project configuration section ---
# Use this section to configure per-project settings
#       (settings that do not change between hosts).
#
# Use local_settings.py to configure per-host settings
#       (such as database settings and admins).


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'mainsite',
    'cachemodel',
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
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
    'mainsite.context_processors.default_context',
]


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


# --- Generic configuration section ---
# This section will usually not need to be modified on a per-project basis.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(TOP_DIR, 'media')

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
    path.join(TOP_DIR, 'templates'),
]

# Project-level fixtures
if path.exists(path.join(PROJECT_DIR, 'fixtures')):
    FIXTURE_DIRS = ['fixtures']


def load_local_settings():
    """
    Load the settings defined in the mainsite.local_settings module.

    Once all settings are loaded, call local_settings.setup with a
    dictionary of the final settings.
    """
    from mainsite import local_settings

    def filter_settings(settings_dict):
        """
        Filters a dict by uppercase keys.  Returns a new dictionary
        which contains only the items which have uppercase keys.
        """
        return dict(
            filter(lambda (k, v): k.isupper(), settings_dict.items())
        )

    settings_dict = globals() # dict of our main settings.

    # Update main settings with the local_settings.
    settings_dict.update(
        # Filter out functions and __special__ keys.
        filter_settings(local_settings.__dict__)
    )

    # If local_settings has a 'setup' function then call it with our
    # final settings dict.
    if hasattr(local_settings, 'setup') and callable(local_settings.setup):
        local_settings.setup(settings_dict)

# Load additional settings from the mainsite.local_settings module,
# if it exists.
try:
    # Check if it exists.
    imp.find_module('local_settings', [PROJECT_DIR])
except ImportError:
    pass
else:
    load_local_settings()
