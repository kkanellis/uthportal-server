#!/bin/bash



#Check if commands are available
command -v python2.7 >/dev/null 2>&1 || { echo >&2 "I require python2.7 but it's not installed.  Aborting."; exit 1; }
command -v virtualenv >/dev/null 2>&1 || { echo >&2 "I require virtualenv but it's not installed.  Aborting."; exit 1; }


#Use first argument for dir.
ENV_DIR=$1

#If argument is unset or empty, use defualt 'venv'
if [ -z "$ENV_DIR" ]; then
    ENV_DIR="uthportal-env"
fi

#Check if dir exists
if [ -d "$ENV_DIR" ]; then
    printf "Directory $ENV_DIR  already exists.\n"
    read -p "Delete?[yY/nN]: " -n 1 -r
    echo #newline

    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -r $ENV_DIR
    else
        echo Aborting.
        exit 0
    fi
fi

PY_PATH="$(which python2.7)"
virtualenv -p ${PY_PATH} $ENV_DIR
