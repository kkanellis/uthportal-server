#!/bin/bash

if [ -d "env" ]; then
    printf "Directory \"env\" already exists.\n"
    read -p "Delete?[yY/nN]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -r env
    else
        echo Abort.
        exit 0
    fi
fi

command -v python2.7 >/dev/null 2>&1 || { echo >&2 "I require python2.7 but it's not installed.  Aborting."; exit 1; }
command -v virtualenv >/dev/null 2>&1 || { echo >&2 "I require virtualenv but it's not installed.  Aborting."; exit 1; }

PY_PATH="$(which python2.7)"
virtualenv -p ${PY_PATH} env
