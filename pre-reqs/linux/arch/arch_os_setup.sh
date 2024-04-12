#!/bin/bash
GPU_PLATFORM=""
FRAMEWORK="" 

function parse_args() {    
    while [ "$#" -gt 0 ]; do
        case "$1" in
            -g|--gpu)
                if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                    GPU_PLATFORM="$2"
                    shift 2
                fi
                ;;
            -f|--framework)
                if [ -n "$3" ] && [ "${3:0:1}" != "-" ]; then
                    FRAMEWORK="$3"
                    shift 2
                fi
                ;;
            -h|--help)
                echo "Usage: $0 [options] <cuda|rocm>"
                echo "Options:"
                echo "  -g, --gpu    Specify the GPU platform (cuda or rocm)"
                echo "  -h, --help   Show this help message and exit"
                exit 0
                ;;
            *)
                echo "Unknown argument: $1"
                echo "Usage: $0 [options] -g <cuda|rocm>"
                exit 1
                ;;
        esac
    done

    echo "Arguments parsed..."
}

# install dependencies arch
function install_dependencies() {
    # check if pamac is installed
    if ! command -v pamac &> /dev/null
    then
        echo "pamac is not installed. Installing pamac..."
        sudo pacman -S pamac --no-confirm
    fi
    # check if docker is installed
    if ! command -v docker &> /dev/null
    then
        echo "docker is not installed. Installing docker..."
         pamac install docker docker-compose --no-confirm
    fi
} 

function install_rocm() {
    # check if rocm is installed
    if ! command -v rocm-smi &> /dev/null
    then
        echo "rocm is not installed. Installing rocm..."
        pamac install rocm-hip-sdk rocm-opencl-runtime rocm-dkms rocm-opencl rocm-opencl-dev rocm-profiler rocm-utils rocm-smi rocm-cmake rocm-device-libs rocm-clang rocm-rocprofiler rocm-rocminfo rocm-bandwidth-test
        pamac install rocm-hip-sdk rocm-opencl-sdk python-pytorch-cxx11abi-opt-rocm --no-confirm
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
    systemctl start docker
    systemctl enable docker
    usermod -aG docker "$USER"
}

function check_os() {
    if [ ! -f /etc/arch-release ]; then
        echo "This script is only for Arch Linux"
        exit 1
    fi
}


function install_ollama() {
    # install ollama check if installed
    if ! command -v ollama &> /dev/null
    then
        echo "ollama is not installed. Installing ollama..."
        sh "ollama/${OLLAMA_VERSION}/ollama_install.sh"
    fi
}


check_os
parse_args "$@"
install_dependencies
if [[ ${GPU_PLATFORM} == "cuda" ]]; then
    install_cuda
    install_nvidia_container_toolkit
elif [[ ${GPU_PLATFORM} == "rocm" ]]; then
    install_rocm
fi
setup_docker
if [[ $FRAMEWORK == "ollama" ]]; then
    install_ollama
fi
