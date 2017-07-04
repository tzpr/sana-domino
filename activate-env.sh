#!/bin/bash
# create and activate python environment for sana-domino project
# script follows loosely https://google.github.io/styleguide/shell.xml

ENV_NAME=sana-domino-env


# add created virtual env folder to .gitignore file
git_ignore_env() {
    echo $ENV_NAME >> .gitignore 
}

# activate created virtual env
activate_env() {
    . ${ENV_NAME}/bin/activate
    echo "* Virtual environment ${ENV_NAME} activated."
}
 
# install needed modules to created virtual env
install_modules() {
    echo "* Installing modules for ${ENV_NAME}..."
    pip install func_timeout 
}

# create virtual env
create_env() {
    echo "* Creating $ENV_NAME..."
    python3 -m venv ${ENV_NAME}
}

# the "main"
if [ -d ${ENV_NAME} ]; then
    activate_env
else
    create_env
   
    if [ -d ${ENV_NAME} ]; then
        install_modules
        activate_env
        git_ignore_env
    else
        echo "** Failed to create environment!"
    fi
fi

