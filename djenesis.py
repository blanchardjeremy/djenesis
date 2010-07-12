#!/usr/bin/env python

"""
djenesis is a toole for inflating a new Django project
"""

import sys
import shutil
import os
import re
import random
import urllib2
import tarfile
import StringIO

from optparse import OptionParser

def generate_secret_key():
    """Generate a random value for settings.SECRET_KEY."""
    return ''.join(
        [random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
            for i in range(50)]
    )


def do_copy(template_dir, destination_dir):
    #print "template: %s\ndestination: %s\n" % (template_dir, destination_dir)
    shutil.copytree(template_dir, destination_dir, symlinks=True)

    secret_key = generate_secret_key()

    settings_path = os.path.join(destination_dir, 'mainsite', 'settings.py')
    if os.path.exists(settings_path):
        settings_file = open(settings_path, 'r')
        settings_data = settings_file.read()
        settings_file.close()
        settings_file = open(settings_path, 'w')
        settings_data = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_data)
        settings_file.write(settings_data)
        settings_file.close()
    else:
        print "Could not locate %s. Did not generate SECRET_KEY" % (settings_path)


    return 0

def main():
    parser = OptionParser(usage="usage: %prog [options] <new-project-directory>")
    parser.add_option("-t", "--template-dir", help="specify a different template directory")
    parser.add_option("-d", "--django-version", help="specify a django version to fetch and extract", default='1.2.1')
    parser.add_option("-u", "--django-url", help="specify the URL to fetch django from")
    parser.add_option("-n", "--no-django", help="Dont fetch django into lib/django automatically", action="store_true", default=False)
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    destination_dir = os.path.abspath(args[0])
    template_dir = options.template_dir
    if template_dir is None:
        template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__).decode('utf-8')), "project_template")
    if not os.path.exists(template_dir):
        print "%s: template directory does not exist!" % (template_dir,)
        sys.exit(1)

    ret = do_copy(template_dir, destination_dir) 
    if ret != 0:
        sys.exit(ret)

    if not options.no_django:
        django_url = options.django_url
        if django_url is None:
            django_url ='http://www.djangoproject.com/download/%s/tarball' % options.django_version

        print "Extracting %s..." % django_url

        tar_buf = StringIO.StringIO()
        uh = urllib2.urlopen(django_url)
        tar_buf.write( uh.read() )
        uh.close()
        tar_buf.seek(0)
        tar = tarfile.open(fileobj=tar_buf, mode='r:gz')
        for item in tar:
            tar.extract(item, path=destination_dir)
        tar.close()
        uh.close()

        symlink_dest = os.path.join(destination_dir,"lib","django")

        if hasattr(os, 'symlink'):
            os.symlink(os.path.join("..","Django-%s"%options.django_version,"django"),symlink_dest)
        else:
            print "Symlinks are not supported on your platform. you need to copy %s to %s manually." % (
                os.path.join(destination_dir, "Django-%s"%options.django_version, "django"),
                os.path.join(destination_dir, "lib", "django"),
                )

    print "Initialized a new djenesis project in %s" % destination_dir
    print "You now need to copy %s to %s and configure it for your local machine" % (
        os.path.join(args[0], "mainsite", "local_settings.py.example"),
        os.path.join(args[0], "mainsite", "local_settings.py"),
        )
        

    

if __name__ == '__main__':
    main()
