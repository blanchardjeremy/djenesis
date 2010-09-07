#!/usr/bin/env python
"""
djenesis is a tool for inflating a new Django project
"""

from optparse import OptionParser
import StringIO
import os
import re
import shutil
import sys
import tarfile
import urllib2
import random


def package_data(file_name):
    return os.path.join(os.path.split(__file__)[0], file_name)


def generate_secret_key():
    """Generate a random value for settings.SECRET_KEY."""
    return ''.join(
        [random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]
    )


def my_copytree(src, dst, symlinks=False, ignore=None):
    """Yanked and forked from python2.6/shutil.py

    Modified to allow destination directory to exist
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                my_copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error, err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error, errors

def do_copy(template_dir, destination_dir):
    #print "template: %s\ndestination: %s\n" % (template_dir, destination_dir)
    my_copytree(template_dir, destination_dir, symlinks=True, ignore=shutil.ignore_patterns('.svn*'))

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
    parser.add_option("-e", "--virtualenv", help="additionally create a virtualenv environment", action="store_true", default=False)
    parser.add_option("", "--env", help="specify the name of the virtualenv directory to create", default="env")
    parser.add_option("", "--code", help="specify the name of the code directory to create", default="code")
    parser.add_option("-r", "--requirements", help="specify a requirements.txt file to bootstrap with")

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    project_dir = os.path.abspath(args[0])
    code_dir = os.path.join(project_dir, options.code)
    env_dir = os.path.join(project_dir, options.env)

    template_dir = options.template_dir
    if template_dir is None:
        #template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__).decode('utf-8')), "project_template")
        template_dir = package_data("project_template")
    if not os.path.exists(template_dir):
        print "%s: template directory does not exist!" % (template_dir,)
        sys.exit(1)

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    ret = do_copy(template_dir, code_dir)
    if ret != 0:
        sys.exit(ret)

#    if not options.no_django:
#        django_url = options.django_url
#        if django_url is None:
#            django_url ='http://www.djangoproject.com/download/%s/tarball' % options.django_version
#
#        print "Extracting %s..." % django_url
#
#        tar_buf = StringIO.StringIO()
#        uh = urllib2.urlopen(django_url)
#        tar_buf.write( uh.read() )
#        uh.close()
#        tar_buf.seek(0)
#        tar = tarfile.open(fileobj=tar_buf, mode='r:gz')
#        for item in tar:
#            tar.extract(item, path=destination_dir)
#        tar.close()
#        uh.close()
#
#        symlink_dest = os.path.join(destination_dir,"lib","django")
#
#        if hasattr(os, 'symlink'):
#            os.symlink(os.path.join("..","Django-%s"%options.django_version,"django"),symlink_dest)
#        else:
#            print "Symlinks are not supported on your platform. you need to copy %s to %s manually." % (
#                os.path.join(destination_dir, "Django-%s"%options.django_version, "django"),
#                os.path.join(destination_dir, "lib", "django"),
#                )
#
    print "Initialized a new djenesis project in %s" % project_dir
    #print "You now need to copy %s to %s and configure it for your local machine" % (
        #os.path.join(args[0], "mainsite", "local_settings.py.example"),
        #os.path.join(args[0], "mainsite", "local_settings.py"),
        #)


if __name__ == '__main__':
    main()
