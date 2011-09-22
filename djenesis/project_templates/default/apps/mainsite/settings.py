import sys
import os


# assume we are ./apps/mainsite/settings.py
APPS_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from mainsite import import_settings


settings_dict = globals()
# import settings from settings_project and add them to globals
settings_dict.update(import_settings('mainsite.settings_project'))

settings_dict.update(import_settings('mainsite.settings_local'))
