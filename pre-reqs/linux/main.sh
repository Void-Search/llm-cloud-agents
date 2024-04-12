#!/bin/bash
### setup script for pre-requisites on linux systems

CONFIG_FILE=""

function log() {
    # print to terminal and log
    echo "$(date) - $1" | tee -a "$LOG_FILE"
}

function check_if_user_has_privellages() {
    # Check if running with sudo
    if [ "$EUID" -ne 0 ]
    then 
        echo "Please run as root"
        exit 1
    fi
}

function parse_args() {    
    while [ "$#" -gt 0 ]; do
        case "$1" in
            -c|--config_file)
                if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                    CONFIG_FILE="$2"
                    shift 2
                fi
                ;;
            -h|--help)
                echo "Usage: $0 [options] <cuda|rocm>"
                echo "Options:"
                echo "  -c, --config_file    Specify the path to the .config file"
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
}

function source_config_file() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log "Config file not found at $CONFIG_FILE. Exiting..."
        exit 1
    fi
    source "$CONFIG_FILE"

}

function check_os() {
    if [ -f /etc/arch-release ] || [ -f /etc/manjaro-release ]; then
        log "Running arch linux setup..."
        if [-f "${PWD}/linux/arch/arch_os_setup.sh"]; then
            bash "${PWD}/linux/arch/arch_os_setup.sh"
        else
            log "${PWD}/linux/arch/arch_os_setup.sh not found. Exiting..."
            exit 1
        fi
    elif [ -f /etc/debian_version ]; then
        log "Running debian/ubuntu setup..."
        if [-f "${PWD}/linux/ubuntu/ubuntu_os_setup.sh"]; then
            bash "${PWD}/linux/ubuntu/ubuntu_os_setup.sh"
        else
            log "${PWD}/linux/ubuntu/ubuntu_os_setup.sh not found. Exiting..."
            exit 1
        fi
    else
        log "Unsupported OS. Exiting..."
        exit 1
    fi
}


function main() {
    check_if_user_has_privellages
    parse_args "$@"
    source_config_file
    log "Configuration parsed..."
    log "Starting pre-requisites installation..."
    check_os

}

main "$@"