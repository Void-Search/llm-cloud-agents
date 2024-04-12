#!/bin/bash

# check if running with sudo
if [ "$EUID" -ne 0 ]
then 
    echo "Please run as root"
    exit 1
fi



function install_nvidia_toolkit() {
    # Add the package repositories
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    # Update the package list
    apt-get update && apt-get upgrade -y

    # Install the NVIDIA driver
    apt-get install -y nvidia-driver-545 docker.io docker-compose nvidia-container-toolkit
    
    # configure the runtime
    nvidia-ctk runtime configure --runtime=docker
    
    # Start and enable the Docker service
    systemctl restart docker
    systemctl enable --now docker


}


install_nvidia_toolkit