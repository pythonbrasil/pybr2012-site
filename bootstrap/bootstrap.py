import sys
import subprocess


# the below syntax works on both 2.6 and 2.7.
print "Bootstraping Virtualenv for Python {0}.{1}".format(*sys.version_info)

script = "bootstrap/bootstrap{0}.{1}.py".format(*sys.version_info)
subprocess.call(['python', script])