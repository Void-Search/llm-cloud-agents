FROM python:3.11-slim

WORKDIR /workspace

COPY . /workspace/
COPY requirements.txt ./

# Install necessary tools, update & clean up in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#  install script
RUN sh ollama_install.sh && \
    rm ollama_install.sh