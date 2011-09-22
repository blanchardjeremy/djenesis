import sys
import os


__all__ = ['APPS_DIR','TOP_DIR','import_settings']

# assume we are ./apps/mainsite/__init__.py
APPS_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

# Path to the whole project (one level up from apps)
TOP_DIR = os.path.dirname(APPS_DIR)

def import_settings(settings_name):
    try:
        __import__(settings_name)

        settings_module = sys.modules[settings_name]

        #update the global settings with all uppercase values from settings_module
        settings_dict = dict(filter(lambda (k, v): k.isupper(), settings_module.__dict__.items())) 

        #call settings_module.setup with a dictionary of the final settings if present
        if callable(getattr(settings_module, 'setup', None)):
            settings_module.setup(settings_dict)

        return settings_dict
    except ImportError as e:
        print(e)
        pass
    return None
