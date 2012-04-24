# coding: utf-8
import os
from os.path import abspath, basename, dirname, join, pardir
import subprocess


def adjust_options(options, args):
    # get current dir
    BOOTSTRAP_PATH = abspath(dirname(__file__))

    # erase args
    while len(args):
        args.pop()

    # set virtualenv's dir
    args.append(join(BOOTSTRAP_PATH, pardir))


def extend_parser(parser):
    # overide default options
    parser.set_defaults(unzip_setuptools=True,
                        use_distribute=True)


def after_install(options, home_dir):
    # Install project requirements
    subprocess.call(['make', 'deps'])
    subprocess.call(['make', 'settings'])
    subprocess.call(['make', 'setup'])

    print \
"""
Ready to develop! Try running the tests:

    make test
    make jasmine

"""