#!/usr/bin/env python

from distutils.core import setup

setup(name='djenesis',
    version='0.9.7',
    description='Bootstrap django projects using a standard project template',
    author='Concentric Sky',
    author_email='django@concentricsky.com',
    url='http://code.google.com/p/djenesis',
    scripts=['scripts/djenesis'],
    packages=['djenesis'],
    package_data={'djenesis': [
        'project_template/apps/.gitignore',
        'project_template/etc/*',
        'project_template/fixtures/.gitignore',
        'project_template/lib/.gitignore',
        'project_template/mainsite/*',
        'project_template/media/css/.gitignore',
        'project_template/media/img/.gitignore',
        'project_template/media/js/.gitignore',
        'project_template/media/uploads/.gitignore',
        'project_template/templates/*',
        ]},
)
