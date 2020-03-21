#!/bin/bash

set -e
pushd $( dirname "${BASH_SOURCE[0]}" ) > /dev/null
source "scripts/bash_utils.sh"
if [ ! -d "$VENV" ]; then
    ./scripts/build.sh
fi
activate_venv

python translate.py "$@"

deactivate
popd > /dev/null