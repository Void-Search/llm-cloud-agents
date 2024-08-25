#!/bin/bash 

# Install Rust


function log() {
    echo -e "\e[32m$1\e[0m"
}

if [ -x "$(command -v rustup)" ]; then
    log "Rust is already installed"
    exit 0
fi


log "Downloading Rust Install Script"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs >> rust_install_script.sh
log "Review script and run it to install Rust ${PWD}/rust_install_script.sh"

