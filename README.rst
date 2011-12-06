========
Djenesis
========


What Djenesis Is
----------------

| Djenesis helps you get started working on a django project, either a brand new one, or one that is already in progress.
| Djenesis has no dependencies other than a standard python install.
| Djenesis leverages virtualenv/pip and helps you manage project dependencies.
| Djenesis allows you to specify your own template, use community templates, or check your project out from your favorite scm (git,svn,hg)


What Djenesis Is Not
--------------------
| Djenesis is not a django app.  It is a python commandline tool.

Installation
------------
If you wish to use Djenesis universally, you can install it like so:

``pip install git+ssh://git@github.com/concentricsky/djenesis.git``

Usage
-----
::

Usage: djenesis <output_directory> [options] [package...]

Options:
  -h, --help            show this help message and exit
  -e ENV_DIRECTORY, --virtualenv=VIRTUALENV
                        Specify the directory to create the virtualenv at
  --no-virtualenv       Don't create a virtualenv
  -t TEMPLATE, --template=TEMPLATE
                        Specify template URL to inflate from


Examples
--------

``djenesis mynewproject``
    | generates ./mynewproject from default template.
    | creates virtualenv at ./env-mynewproject and installs latest Django


``djenesis foobar --no-virtualenv``
    | generates ./foobar from default template.
    | no virtualenv is created.

``djenesis theproject/code --virtualenv=theproject/env Django==1.1 psycopg2``
    | generates ./theproject/code from the default template.
    | initializes a virtualenv at ./theproject/env and installs Django-1.1 and psycopg2

``djenesis mynewproject -e ~/.virtualenvs/mynewproject -t http://example.com/django/random-django-template.tar.gz``
    | downloads and extracts the tar file into ./mynewproject
    | generates a virtualenv at ~/.virtualenvs/mynewproject
    | checks the template for a requirements.txt, if present will pip install all packages into the virtualenv.

``djenesis mywip/code -e mywip/env -t git+git@github.com:wittyusername/respository.git``
    | uses git to clone the repository into ./mywip/code
    | generates a virtualenv at ./mywip/env
    | if requirements.txt exists at toplevel directory in repo, pip installs any packages present.

``djenesis mynewproject/code -e mynewproject/env --template=~/projects/django-templates/normal``
    | copies the project template from a local directory at ~/projects/django-templates/normal into ./mynewproject/code
    | generates a virtualenv at ./mynewproject/env
    | checks the template for a requirements.txt, if present will pip install all packages into the virtualenv.

Default Project Structure
-------------------------
If you do not specify a template when you invoke Djenesis, it will inflate its default project structure. 
For example if you called the command ``djenesis mynewproject`` the following directory structure would be created::

    ./mynewproject
        ./mynewproject/manage.py
        ./mynewproject/requirements.txt
        ./mynewproject/apps
        ./mynewproject/apps/mainsite/settings.py
        ./mynewproject/apps/mainsite/local_settings.py.example
        ./mynewproject/apps/mainsite/urls.py
        ./mynewproject/apps/mainsite/views.py
        ./mynewproject/apps/mainsite/media/css/screen.css
        ./mynewproject/apps/mainsite/templates/base.html
        ./mynewproject/apps/mainsite/templates/500.html
        ./mynewproject/apps/mainsite/templates/404.html
        ./mynewproject/etc/django.wsgi
        ./mynewproject/etc/fixtures/
        ./mynewproject/uploads/
        ./mynewproject/static/

| You'll notice that ``mainsite`` is the default point for all things django related.
| Only the ``apps`` directory is added to the PYTHON_PATH.



