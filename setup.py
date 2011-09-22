#!/usr/bin/env python

from distutils.core import setup
import djenesis

setup(name='djenesis',
    version='.'.join(map(str, djenesis.VERSION)),
    description='Bootstrap django projects using standard project templates',
    author='Concentric Sky',
    author_email='django@concentricsky.com',
    url='http://github.com/concentricsky/djenesis',
    scripts=['scripts/djenesis'],
    packages=['djenesis'],
    package_data={'djenesis': [
        'project_templates/default/.gitignore',
        'project_templates/default/manage.py',
        'project_templates/default/apps/mainsite/*',
        'project_templates/default/templates/*',
        'project_templates/default/media/css/.gitignore',
        'project_templates/default/media/img/.gitignore',
        'project_templates/default/media/js/.gitignore',
        'project_templates/default/media/uploads/.gitignore',
        'project_templates/default/fixtures/.gitignore',
        ]},
)
