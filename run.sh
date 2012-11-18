#!/bin/bash

source /home/pythonbrasil/env/bin/activate

cd /home/pythonbrasil/pythonbrasil8
export DJANGO_SETTINGS_MODULE=pythonbrasil8.settings_local

python $@
cd $OLDPWD
