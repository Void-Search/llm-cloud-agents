#!/bin/bash
# build script to setup everything for ollama
#

GPU_PLATFORM=""
OVERWRITE_MODELS=""
SCRIPT_DIR=$(dirname "$SCRIPT_NAME")
# ollama build script
# check if running with sudo
if [ "$EUID" -ne 0 ]
then
    echo "Please run as root"
    exit 1
fi


# Function to parse command line arguments
function parse_args() {
    while getopts "g:f:" opt; do
        case ${opt} in
            g )
                GPU_PLATFORM=$OPTARG  # Set GPU platform based on argument value
                ;;
            f )
                OVERWRITE_MODELS=$OPTARG  # Set overwrite models flag based on argument value
                ;;
            \? )
                echo "Usage: cmd [-g GPU_PLATFORM] [-f OVERWRITE_MODELS]"
                exit 1
                ;;
        esac
    done
}

# check if running on arch
function pre_req(){
    if [ ! -f /etc/arch-release ]; then
        echo "Installing pre-requisites for Arch Linux"
        sh pre-reqs/arch_os_setup.sh -g $GPU_PLATFORM -f "ollama"
    else
        echo "No OS support for this script"
        exit 1
    fi
}

function get_models(){
    
    # download models with ollama
    if ! command -v ollama &> /dev/null
    then
        echo "ollama is not installed. Installing ollama..."
        exit 1
    fi
    # loop through list download models
    for model in "$@"
    do
    # check if model exists and we want to overwrite
        if [ -d "$SCRIPT_DIR/models/$model" ] && [ "$OVERWRITE_MODELS" == "true" ]
        then
            rm -rf "$SCRIPT_DIR/models/$model"
            ollama pull "$model"
        elif [ ! -d "$SCRIPT_DIR/models/$model" ]
        then
            ollama pull "$model"
        fi
        ollama cp "$model" "$SCRIPT_DIR/models"
    done
}

function run_docker_compose(){
    # clean up docker-compose if running
    docker-compose down
    docker-compose rm
    docker-compose pull
    docker-compose build
    docker-compose up -d
}

function main(){
    parse_args "$@"
    pre_req
    get_models "llama2"
    run_docker_compose
}

