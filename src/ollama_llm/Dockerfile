# Stage 1: Build and install dependencies
ARG ROCM_VERSION=6.0-complete
ARG UBUNTU_VERSION=22.04

FROM rocm/dev-ubuntu-${UBUNTU_VERSION}:${ROCM_VERSION} AS build-env
WORKDIR /workspace
COPY . /workspace/
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Sydney
RUN apt-get update && \
    apt-get install -y --no-install-recommends \ 
    build-essential \
    ca-certificates \
    cmake-curses-gui \
    curl \
    file \
    git \
    gnupg \
    hipblas-dev \
    kmod \
    libclblast-dev \
    libclc-dev \
    libelf1 \
    libnuma-dev \
    libopenblas-dev \
    libopencl-clang-dev \
    ocl-icd-opencl-dev \
    opencl-c-headers \
    opencl-clhpp-headers \
    opencl-headers \
    python3 \
    python3-pip \
    rocblas-dev \
    rocm-dev \
    software-properties-common \
    vim-nox && \   
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && \
    pip  --no-cache-dir -r requirements.txt 




# Stage 2: Install Ollama
FROM build-env AS ollama_install
WORKDIR /workspace
RUN sh /workspace/ollama_files/ollama_install.sh && \
    rm -rf /workspace/ollama_files && \
    ls -l /usr/local/bin/ollama && \
    chmod +x /usr/local/bin/ollama 

# # Final Stage: Prepare the runtime environment
# FROM ollama_install AS runtime
# WORKDIR /workspace
# ENV PATH="/opt/rocm/bin:/usr/local/bin:${PATH}"
# ENV LD_LIBRARY_PATH="/opt/rocm/lib:/opt/rocm/lib64:${LD_LIBRARY_PATH}"
# ENV HSA_OVERRIDE_GFX_VERSION=10.3.0
# ENV LLAMA_OPENBLAS=1
# ENV LLAMA_CLBLAST=0
# ENV LLAMA_HIPBLAS=1
# ENV CC=/opt/rocm/llvm/bin/clang
# ENV CXX=/opt/rocm/llvm/bin/clang++
# COPY --from=ollama_install /workspace /workspace
# COPY --from=ollama_install /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
# COPY --from=ollama_install /usr/local/bin/ollama /usr/local/bin/ollama
# COPY --from=ollama_install /opt/rocm /opt/rocm
# CMD ["/bin/bash"]