from fabric.api import cd, env, run

import os


env.project_root = '/home/pythonbrasil/pythonbrasil8'
env.app_root = os.path.join(env.project_root, 'pythonbrasil8')
env.virtualenv = '/home/pythonbrasil/env'


def update_app():
    with cd(env.project_root):
        run("git pull")


def collect_static_files():
    with cd(env.app_root):
        run("%(virtualenv)s/bin/python manage.py collectstatic -v 0 --noinput" % env)


def pip_install():
    run("%(virtualenv)s/bin/pip install -r %(project_root)s/requirements.txt" % env)


def start():
    with cd(env.app_root):
        run('%(virtualenv)s/bin/gunicorn_django -p gunicorn.pid --bind=127.0.0.1:8080 --daemon --workers=3' % env)


def reload():
    run('kill -HUP `cat %(app_root)s/gunicorn.pid`' % env)


def stop():
    run('kill -9 `cat %(app_root)s/gunicorn.pid`' % env)


def syncdb():
    with cd(env.app_root):
        run("%(virtualenv)s/bin/python manage.py syncdb --noinput" % env)
        run("%(virtualenv)s/bin/python manage.py migrate --noinput" % env)


def loaddata():
    with cd(env.app_root):
        run("%s/bin/python manage.py loaddata fixtures/initial_data.json" % env.virtualenv)


def limpar_pycs():
    with cd(env.app_root):
        run("find . -name \"*.pyc\" | xargs rm -f ")


def deploy():
    update_app()
    pip_install()
    limpar_pycs()
    collect_static_files()
