VENV=".venv"

detect_python3() {
    min_version="3"
    unset cmd
    if [ ! -z "`python3 --version 2>/dev/null`" ]; then
        cmd=python3
    elif [ ! -z "`py3 --version 2>/dev/null`" ]; then
        cmd=py3
    elif [ ! -z "`python --version 2>/dev/null`" ]; then
        cmd=python
    fi
    if [ -z "$cmd" ] || [ `$cmd --version | sed "s/Python //"` \< $min_version ]; then
        echo "Please install the latest version of Python3" 1>&2
        return 1
    else
        echo "$cmd"
    fi
}

activate_venv() {
    if [ ! -d "$VENV" ]; then
        python_cmd=`detect_python3`
        "$python_cmd" -m venv "$VENV"
    fi
    WIN_VENV_PATH="./${VENV}/Scripts/activate"
    LINUX_VENV_PATH="./${VENV}/bin/activate"
    if [ -f $WIN_VENV_PATH ]; then
        source "${WIN_VENV_PATH}"
    else
        source "${LINUX_VENV_PATH}"
    fi
}

clean_venv() {
    rm -rf "$VENV"
}
