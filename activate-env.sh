#!/bin/sh
# set and activate custom python environment for sana-domino project

ENV_NAME=sana-domino-env


if [ -d ${ENV_NAME} ]; then
    . ${ENV_NAME}/bin/activate
    echo "* Virtual environment ${ENV_NAME} activated."
else
    echo "* Creating $ENV_NAME..."
    python3 -m venv ${ENV_NAME}
    if [ -d ${ENV_NAME} ]; then
        . ${ENV_NAME}/bin/activate
        echo "* Installing modules for ${ENV_NAME}..."
        pip install func_timeout
        echo "* Virtual environment ${ENV_NAME} activated."
    else
        echo "** Failed to create environment!"
    fi
fi

