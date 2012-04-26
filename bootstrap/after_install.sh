#!/bin/bash
set -e

ROOT=`dirname $0`/..

source $ROOT/bin/activate
make deps
make settings
make setup

echo -e "
Ready to go!
Now activate your virtualenv and run some tests.

\tsource bin/activate
\tmake test
\tmake jasmine
"
