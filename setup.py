#!/usr/bin/env python

from distutils.core import setup

setup(name='djenesis',
    version='0.9.6',
    description='Bootstrap django projects using a standard project template',
    author='Concentric Sky',
    author_email='django@concentricsky.com',
    url='http://code.google.com/p/djenesis',
    scripts=['scripts/djenesis'],
    packages=['djenesis'],
    package_data={'djenesis': [
        'project_template/apps/*'
        'project_template/etc/*',
        'project_template/fixtures/*',
        'project_template/lib/*',
        'project_template/mainsite/*',
        'project_template/media/css/*',
        'project_template/media/img/*',
        'project_template/media/js/*',
        'project_template/media/uploads/*',
        'project_template/templates/*',
        ]},
)
