# coding: utf-8
import sys
import virtualenv

# the below syntax works on both 2.6 and 2.7.
filename = "bootstrap{0}.{1}.py".format(*sys.version_info)

extension = open('venv-extension.py').read()
output = virtualenv.create_bootstrap_script(extension)

f = open(filename, 'w').write(output)
