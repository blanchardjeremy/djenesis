#!/usr/bin/env python
"""
djenesis is a tool for inflating a new Django project
"""

import optparse
import StringIO
import os
import random
import re
import shutil
import subprocess
import sys
import tarfile
import urllib2


def package_data(file_name):
    return os.path.join(os.path.split(__file__)[0], file_name)


def call_pip(env_dir, *args):
    pip_path = os.path.join(env_dir, 'bin', 'pip')
    try:
        return subprocess.call(' '.join((pip_path,) + args), shell=True)
    except OSError, e:
        print >> sys.stderr, "Execution failed", e
    return -1


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
    parser = optparse.OptionParser(usage="usage: %prog [options] <new-project-directory> [package...]")
    parser.add_option("-t", "--template-dir", help="specify a different template directory")
    parser.add_option("-e", "--virtualenv", help="additionally create a virtualenv environment", action="store_true", default=False)
    parser.add_option("", "--env", help="specify the name of the virtualenv directory to create", default="env")
    parser.add_option("", "--code", help="specify the name of the code directory to create", default="code")
    parser.add_option("-r", "--requirements", help="specify a requirements.txt file to bootstrap with")

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    if options.requirements or len(args) > 1:
        options.virtualenv = True

    project_dir = os.path.abspath(args[0])
    code_dir = os.path.join(project_dir, options.code)
    env_dir = os.path.join(project_dir, options.env)

    template_dir = options.template_dir
    if template_dir is None:
        template_dir = package_data("project_template")
    if not os.path.exists(template_dir):
        print "%s: template directory does not exist!" % (template_dir,)
        sys.exit(1)

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    ret = do_copy(template_dir, code_dir)
    if ret != 0:
        sys.exit(ret)

    if options.virtualenv:
        try:
            import virtualenv
            #monkey patching in the logger is required here...
            virtualenv.logger = virtualenv.Logger([(virtualenv.Logger.level_for_integer(2), sys.stdout)])
            virtualenv.create_environment(env_dir, site_packages=False, clear=True, use_distribute=True)
        except ImportError:
            print "Failed to import virtualenv, is it installed?"
            sys.exit(1)

    if options.requirements or len(args) > 1:
        #activate the virtualenv environment
        activate_file = os.path.join(env_dir, 'bin', 'activate_this.py')
        execfile(activate_file, dict(__file__=activate_file))

    if options.requirements:
        call_pip(env_dir, 'install', '-r', options.requirements)

    if len(args) > 1:
        call_pip(env_dir, *(('install',) + tuple(args[1:])))


if __name__ == '__main__':
    main()