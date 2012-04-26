# coding: utf-8
from os.path import join, dirname
import subprocess


# Install project requirements
AFTER_INSTALL = join(dirname(__file__), 'after_install.sh')

def after_install(options, home_dir):
    subprocess.call([AFTER_INSTALL])
