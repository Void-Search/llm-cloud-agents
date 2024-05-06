#!/bin/bash

source "${PWD}/pod.conf"
LOG_FILE="pod_setup.log"

# Check if runpodctl is installed
if ! command -v runpodctl &> /dev/null; then
    echo "runpodctl could not be found"
    exit 1
fi

# Define the create_pod function
create_pod() {
    echo "Attempting to create pod..."
    runpodctl create pod \
    --name "${NAME}" \
    --imageName "${IMAGE_TYPE}" \
    --vcpu "${CPU_COUNT}" \
    --mem "${MEMORY_SIZE}" \
    --gpuCount "${GPU_COUNT}" \
    --gpuType "${GPU_TYPE}" \
    --ports "${PORTS}" \
    --containerDiskSize "${CONTAINER_DISK_SIZE}"
    if [ $? -eq 0 ]; then
        echo "Pod created successfully."
        exit 0
    else
        echo "Pod creation failed, retrying with backup GPU."
        runpodctl create pod \
        --name "${NAME}" \
        --imageName "${IMAGE_TYPE}" \
        --vcpu "${CPU_COUNT}" \
        --mem "${MEMORY_SIZE}" \
        --gpuCount "${GPU_COUNT}" \
        --gpuType "${BACKUP_GPU_TYPE}" \
        --ports "${PORTS}" \
        --containerDiskSize "${CONTAINER_DISK_SIZE}"
        if [ $? -eq 0 ]; then
            echo "Pod created successfully with backup GPU."
            exit 0
        else
            echo "Pod creation failed with both primary and backup GPUs."
            exit 1
        fi
    fi
}

# Define the stop_pod function
stop_pod() {
    echo "Attempting to stop pod..."
    runpodctl stop pod $(runpodctl get pod | grep "${NAME}" | awk '{ print $1}')
    if [ $? -eq 0 ]; then
        echo "Pod stopped successfully."
    else
        echo "Failed to stop pod."
    fi
}

# Command-line argument processing
case "$1" in
    create)
        shift # Remove 'create' from the argument list
        while getopts "n:i:c:m:g:t:p:d:b:" opt; do
            case "$opt" in
                n) NAME="$OPTARG" ;;
                i) IMAGE_TYPE="$OPTARG" ;;
                c) CPU_COUNT="$OPTARG" ;;
                m) MEMORY_SIZE="$OPTARG" ;;
                g) GPU_COUNT="$OPTARG" ;;
                t) GPU_TYPE="$OPTARG" ;;
                p) PORTS="$OPTARG" ;;
                d) CONTAINER_DISK_SIZE="$OPTARG" ;;
                b) BACKUP_GPU_TYPE="$OPTARG" ;;
                *) echo "Invalid option: -$OPTARG"
                   exit 1 ;;
            esac
        done
        create_pod
        ;;
    stop)
        shift # Remove 'stop' from the argument list
        while getopts "n:" opt; do
            case "$opt" in
                n) NAME="$OPTARG" ;;
                *) echo "Invalid option: -$OPTARG"
                   exit 1 ;;
            esac
        done
        stop_pod
        ;;
    *)
        echo "Usage: $0 {create|stop} [options]"
        echo "Options for 'create':"
        echo "  -n NAME                     Name of the pod to manage"
        echo "  -i IMAGE_TYPE               Type of image for the pod"
        echo "  -c CPU_COUNT                Number of CPUs for the pod"
        echo "  -m MEMORY_SIZE              Memory size for the pod"
        echo "  -g GPU_COUNT                Number of GPUs for the pod"
        echo "  -t GPU_TYPE                 Type of the primary GPU for the pod"
        echo "  -p PORTS                    Ports to be opened on the pod"
        echo "  -d CONTAINER_DISK_SIZE      Disk size for the pod container"
        echo "  -b BACKUP_GPU_TYPE          Backup GPU type if primary fails"
        echo "Options for 'stop':"
        echo "  -n NAME                     Name of the pod to stop"
        exit 1
        ;;
esac
