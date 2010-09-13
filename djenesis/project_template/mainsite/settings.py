import imp
import sys
import os


# Path to the django project (mainsite)
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
# Path to the whole project (one level up from mainsite)
TOP_DIR = os.path.abspath(os.path.dirname(PROJECT_DIR).decode('utf-8'))
# Required python libraries should go in this directory
LIB_DIR = os.path.join(TOP_DIR, "lib")
# Apps written for the project go in this directory
APP_DIR = os.path.join(TOP_DIR, "apps")
# Prepend LIB_DIR, PROJECT_DIR, and APP_DIR to the PYTHONPATH
for p in (PROJECT_DIR, LIB_DIR, APP_DIR, TOP_DIR):
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

# Project-level fixtures
if os.path.exists(os.path.join(PROJECT_DIR, 'fixtures')):
    FIXTURE_DIRS = ['fixtures']


def filter_settings(settings_dict):
    """
    Filters a dict by uppercase keys.  Returns a new dictionary
    which contains only the items which have uppercase keys.
    """
    return dict(
        filter(lambda (k, v): k.isupper(), settings_dict.items())
    )


def load_app_settings():
    """ Iterate over INSTALLED_APPS and load any settings.py """
    settings_dict = globals()
    for app in INSTALLED_APPS:
        #skip mainsite or builtin django apps
        if app == 'mainsite' or app[:7] == 'django.':
            continue

        try:
            #import the app's settings module
            settings_module = '%s.settings' % (app,)
            __import__(settings_module)

            #update our settings with app's settings
            settings_dict.update(
                filter_settings(sys.modules[settings_module].__dict__)
            )
        except ImportError:
            pass


def load_local_settings():
    """
    Load the settings defined in the mainsite.local_settings module.

    Once all settings are loaded, call local_settings.setup with a
    dictionary of the final settings.
    """
    from mainsite import local_settings

    settings_dict = globals()  # dict of our main settings.

    # Update main settings with the local_settings.
    settings_dict.update(
        # Filter out functions and __special__ keys.
        filter_settings(local_settings.__dict__)
    )

    # If local_settings has a 'setup' function then call it with our
    # final settings dict.
    if hasattr(local_settings, 'setup') and callable(local_settings.setup):
        local_settings.setup(settings_dict)

# Load any settings from INSTALLED_APPS
load_app_settings()

# Load additional settings from the mainsite.local_settings module,
# if it exists.
try:
    # Check if it exists.
    imp.find_module('local_settings', [PROJECT_DIR])
except ImportError:
    pass
else:
    load_local_settings()