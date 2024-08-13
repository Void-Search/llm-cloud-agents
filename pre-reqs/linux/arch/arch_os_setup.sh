#!/bin/bash
GPU_PLATFORM=""
FRAMEWORK="" 
LOG_FILE="${PWD}/arch_os_setup.log"

function log() {
    # print to terminal and log
    echo "$(date) - $1" | tee -a "$LOG_FILE"
}

function parse_args() {
    while [ "$#" -gt 0 ]; do
        case "$1" in
            -l|--logfile)
                if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                    LOG_FILE="$2"
                    log "Log File: $LOG_FILE"
                    shift 2
                else
                    log "Error: Log file path $1 is missing or requires a valid path."
                    exit 1
                fi
                ;;
            -g|--gpu)
                if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                    if [[ "$2" == "cuda" || "$2" == "rocm" ]]; then
                        GPU_PLATFORM="$2"
                        log "GPU Platform: $GPU_PLATFORM"
                        shift 2
                    else
                        log "Error: GPU platform must be 'cuda' or 'rocm'."
                        exit 1
                    fi
                else
                    log "Error: GPU platform $1 is missing or requires a valid argument such as 'cuda' or 'rocm'."
                    exit 1
                fi
                ;;
            -f|--framework)
                if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                    if [[ "$2" == "ollama" ]]; then
                        FRAMEWORK="$2"
                        log "Framework: $FRAMEWORK"
                        shift 2
                    else
                        log "Error: Framework must be 'ollama'."
                        exit 1
                    fi
                else
                    log "Error: Framework $1 is missing or requires a valid argument such as ollama."
                    exit 1
                fi
                ;;
            -h|--help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  -g, --gpu       Specify the GPU platform (cuda or rocm)"
                echo "  -f, --framework Specify the framework to use (only ollama is supported)"
                echo "  -l, --logfile   Specify the path to the log file"
                echo "  -h, --help      Show this help message and exit"
                exit 0
                ;;
            *)
                echo "Unknown argument: $1"
                echo "Usage: $0 [options] -g <cuda|rocm> -f <framework> -l <path to log file>"
                exit 1
                ;;
        esac
    done

    log "Arguments parsed..."
}


# install dependencies arch
function install_dependencies() {
    # check if pamac is installed
    if ! command -v pamac &> /dev/null
    then
        log "pamac is not installed. Installing pamac..."
        sudo pacman -Syu pamac --no-confirm
    fi
    # check if docker is installed
    if ! command -v docker &> /dev/null
    then
        log "docker is not installed. Installing docker..."
         pamac install docker docker-compose --no-confirm
    fi
} 

function install_rocm() {
    # check if rocm is installed
    if ! command -v rocm-smi &> /dev/null
    then
        log "rocm is not installed. Installing rocm..."
        pamac install rocm-hip-sdk \
              rocm-smi-lib \
              rocm-opencl-runtime \
              rocm-smi-lib \
              rocm-cmake \
              rocm-device-libs \
              rocm-clang-ocl \
              rocm-language-runtime \
              python-pytorch-opt-rocm \
              rocm-opencl-sdk \
              ollama-rocm \
              rocm-core \
              --no-confirm
        useradd rocm_user
        groupadd -g 985 video
        groupadd -g 989 render
        usermod -aG video,render rocm_user
    fi
}

function install_cuda() {
    pamac install cuda cudnn --no-confirm
}

function install_nvidia_container_toolkit() { 
    pamac install nvidia-container-toolkit --no-confirm
}
    

function setup_docker() {
    systemctl enable --now docker
    usermod -aG docker "$USER"
}

function check_os() {
    if [ ! -f /etc/arch-release ]; then
        log "This script is only for Arch Linux"
        exit 1
    fi
}


function install_ollama() {
    # install ollama check if installed
    if [! command -v ollama &> /dev/null]; then
        log "ollama is not installed. Installing ollama..."
        curl -fsSL "https://ollama.com/install.sh" | sh
    fi
}


check_os
parse_args "$@"
install_dependencies
if [[ ${GPU_PLATFORM} == "cuda" ]]; then
    log "Installing cuda..."
    install_cuda
    install_nvidia_container_toolkit
elif [[ ${GPU_PLATFORM} == "rocm" ]]; then
    log "Installing rocm..."
    install_rocm
fi
setup_docker
if [[ $FRAMEWORK == "ollama" ]]; then
    log "Installing ollama..."
    install_ollama
fi
