#!/usr/bin/env python

from distutils.core import setup
import os


def walk_data_files(output_path, scan_dir):
    """Use os.walk() to build a data_files definition for setup()"""
    data_files = []
    for dirname, dirs, files in os.walk(scan_dir):
        files = filter(lambda f: not any([f.startswith('.'), f.endswith('.pyc')]), files)
        if len(files) > 0:
            output_dirname = os.path.join(output_path,dirname)
            files = [os.path.join(dirname, f) for f in files]
            data_files.append( (output_dirname, files) )
    return data_files

setup(name='djenesis',
    version='0.9.9',
    description='Bootstrap django projects using standard project templates',
    author='Concentric Sky',
    author_email='django@concentricsky.com',
    url='http://github.com/concentricsky/djenesis',
    scripts=['scripts/djenesis'],
    data_files=walk_data_files('share/djenesis', 'templates'),
)
