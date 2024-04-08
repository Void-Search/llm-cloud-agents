
GPU_PLATFORM=""
function parse_args() {    
    while [ "$#" -gt 0 ]; do
        case "$1" in
            -g|--gpu)
                if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                    GPU_PLATFORM="$2"
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
    pamac install docker docker-compose --no-confirm
} 

function install_rocm() {
    pamac install rocm-hip-sdk rocm-opencl-sdk python-pytorch-cxx11abi-opt-rocm --no-confirm
    usermod -a -G render $USER
    usermod -a -G video $USER
}

function install_cuda() {
    pamac install cuda cudnn --no-confirm
}

function setup_docker() {
    systemctl start docker
    systemctl enable docker
    usermod -aG docker $USER
}

function check_os() {
    # Check if running with sudo
    if [ "$EUID" -ne 0 ]
        then echo "Please run as root"
        exit 1
    fi
    if [ ! -f /etc/arch-release ]; then
        echo "This script is only for Arch Linux"
        exit 1
    fi
}



check_os
parse_args "$@"
install_dependencies
if [[ ${GPU_PLATFORM} == "cuda" ]]; then
    install_cuda
elif [[ ${GPU_PLATFORM} == "rocm" ]]; then
    install_rocm
fi
setup_docker

