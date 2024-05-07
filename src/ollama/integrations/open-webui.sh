#!/bin/bash



# Run the Open WebUI integration in a docker container
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

# make sure ollama is running
docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama --net=host -p 11434:11434 --name ollama ollama/ollama:rocm