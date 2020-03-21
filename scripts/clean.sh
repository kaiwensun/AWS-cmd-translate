#!/bin/bash

set -e
pushd $( dirname "${BASH_SOURCE[0]}" )/.. > /dev/null
source "scripts/bash_utils.sh"
clean_venv
popd > /dev/null
