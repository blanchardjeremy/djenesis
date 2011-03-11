#!/usr/bin/env python

from distutils.core import setup
import djenesis

setup(name='djenesis',
    version='.'.join(map(str, djenesis.VERSION)),
    description='Bootstrap django projects using standard project templates',
    author='Concentric Sky',
    author_email='django@concentricsky.com',
    url='http://code.google.com/p/djenesis',
    scripts=['scripts/djenesis'],
    packages=['djenesis'],
    package_data={'djenesis': [
        'project_templates/default/.gitignore',
        'project_templates/default/etc/*',
        'project_templates/default/mainsite/*',
        'project_templates/default/templates/*',
        'project_templates/default/media/css/.gitignore',
        'project_templates/default/media/img/.gitignore',
        'project_templates/default/media/js/.gitignore',
        'project_templates/default/media/uploads/.gitignore',
        'project_templates/default/apps/.gitignore',
        'project_templates/default/fixtures/.gitignore',
        'project_templates/default/lib/.gitignore',

        'project_templates/csky/.gitignore',
        'project_templates/csky/requirements.txt',
        'project_templates/csky/fabfile.py',
        'project_templates/csky/etc/*',
        'project_templates/csky/mainsite/*',
        'project_templates/csky/templates/*',
        'project_templates/csky/media/css/.gitignore',
        'project_templates/csky/media/img/.gitignore',
        'project_templates/csky/media/js/.gitignore',
        'project_templates/csky/media/uploads/.gitignore',
        'project_templates/csky/apps/.gitignore',
        'project_templates/csky/fixtures/.gitignore',
        'project_templates/csky/lib/.gitignore',

        ]},
)
