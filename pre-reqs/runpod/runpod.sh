#!/bin/bash

RUNPODCTL_BINDIR=$(dirname "$(readlink -fn "$0")")
COMPLETION_SHELL="bash"
API_KEY=""
RUNPOD_VERSION="v1.14.3"
# parse arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        -h|--help)
            echo "Usage: $0"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0"
            exit 1
            ;;
    esac
done

# check if arch linux
if [ -f /etc/arch-release ]
then
    RUNPODCTL_BINDIR=${HOME}/.local/bin
    COMPLETION_SHELL="zsh"
else
    RUNPODCTL_BINDIR="/usr/bin"
fi

function fetch_runpodctl() {
    wget  --show-progress https://github.com/Run-Pod/runpodctl/releases/download/${RUNPOD_VERSION}/runpodctl-linux-amd64 \
     -O runpodctl && \
     chmod +x runpodctl && \
     mv runpodctl "${RUNPODCTL_BINDIR}/runpodctl"
}

function install_completion() {
    if [ "${COMPLETION_SHELL}" = "bash" ]
    then
        runpodctl completion bash > /etc/bash_completion.d/runpodctl
    elif [ "${COMPLETION_SHELL}" = "zsh" ]
    then
        runpodctl completion zsh >> "${HOME}/.zshrc"
    else
        echo "Unsupported shell. Only bash and zsh are supported."
    fi
}

function setup_api_key () {
    echo "Please enter your API key "
    read -r API_KEY
    runpodctl config --apiKey "${API_KEY}"
    # check runpodctl is working
    runpodctl version
    if echo $? > /dev/null; then
        echo "API key setup successfully."
    else
        echo "API key setup failed."
        exit 1

    fi

}

fetch_runpodctl
install_completion
setup_api_key



echo "Runpodctl installed successfully."