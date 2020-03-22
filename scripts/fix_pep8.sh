#!/bin/bash
set -e
pushd $( dirname "${BASH_SOURCE[0]}" )/.. > /dev/null
source "./scripts/bash_utils.sh"
activate_venv

read -n1 -p "Would you like to make changes to files inplace? [Y/n]" answer
printf "\nprocessing...\n"
if [[ $answer == Y || $answer == y ]]
then
    option="--in-place"
else
    option="--diff"
fi

autopep8 $option -r --exclude=".$VENV,./config/local_settings.py,./config/settings.py"  -a .

deactivate
popd > /dev/null
