#!/bin/bash

set -e
if [ ! -z `which readlink` ]; then
    pushd $( dirname $( readlink "${BASH_SOURCE[0]}" )) > /dev/null
else
    pushd $( dirname "${BASH_SOURCE[0]}" ) > /dev/null
fi
source "scripts/bash_utils.sh"
if [ ! -d "$VENV" ]; then
    ./scripts/build.sh
fi
activate_venv

python translate.py "$@"

deactivate
popd > /dev/null