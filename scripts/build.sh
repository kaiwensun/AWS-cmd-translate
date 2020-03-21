#!/bin/bash

set -e
pushd $( dirname "${BASH_SOURCE[0]}" )/.. > /dev/null
source "scripts/bash_utils.sh"
activate_venv

python -m pip install --upgrade pip
pip install -r config/requirements.txt

deactivate
popd > /dev/null
