  
#!/bin/bash
set -e
pushd $( dirname "${BASH_SOURCE[0]}" )/.. > /dev/null
source "./scripts/bash_utils.sh"
activate_venv

pycodestyle --exclude=.venv,./config/local_settings.py,./config/settings.py .

deactivate
popd > /dev/null
