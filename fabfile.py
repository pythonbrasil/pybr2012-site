# -*- coding: utf-8 -*-
import os

from fabric.api import cd, env, run

env.project_root = '/home/pythonbrasil/pythonbrasil8'
env.app_root = os.path.join(env.project_root, 'pythonbrasil8')
env.virtualenv = '/home/pythonbrasil/env'
env.hosts = ['2012.pythonbrasil.org.br']
env.user = 'pythonbrasil'


def update_app(tag):
    with cd(env.project_root):
        run("git pull origin %s" % tag)


def collect_static_files():
    with cd(env.project_root):
        run("DJANGO_SETTINGS_MODULE=pythonbrasil8.settings_local %(virtualenv)s/bin/python manage.py collectstatic -v 0 --noinput" % env)


def pip_install():
    run("%(virtualenv)s/bin/pip install -r %(project_root)s/requirements.txt" % env)


def start():
    with cd(env.project_root):
        run('DJANGO_SETTINGS_MODULE=pythonbrasil8.settings_local %(virtualenv)s/bin/gunicorn --access-logfile=gunicorn-access.log --error-logfile=gunicorn-error.log --pid=gunicorn.pid --bind=127.0.0.1:8080 --daemon --workers=3 pythonbrasil8.wsgi:application' % env)


def reload():
    run('kill -HUP `cat %(project_root)s/gunicorn.pid`' % env)


def stop():
    run('kill -KILL `cat %(project_root)s/gunicorn.pid`' % env)


def syncdb():
    with cd(env.project_root):
        run("DJANGO_SETTINGS_MODULE=pythonbrasil8.settings_local %(virtualenv)s/bin/python manage.py syncdb --noinput" % env)
        run("DJANGO_SETTINGS_MODULE=pythonbrasil8.settings_local %(virtualenv)s/bin/python manage.py migrate --noinput" % env)


def translate():
    with cd(env.app_root):
        run("%(virtualenv)s/bin/django-admin.py compilemessages" % env)


def loaddata():
    with cd(env.project_root):
        run("DJANGO_SETTINGS_MODULE=pythonbrasil8.settings_local %s/bin/python manage.py loaddata fixtures/initial_data.json" % env.virtualenv)


def limpar_pycs():
    with cd(env.project_root):
        run("find . -name \"*.pyc\" | xargs rm -f ")


def deploy(tag="master"):
    update_app(tag)
    pip_install()
    limpar_pycs()
    collect_static_files()
    translate()
