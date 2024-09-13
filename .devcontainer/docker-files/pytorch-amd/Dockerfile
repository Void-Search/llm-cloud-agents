FROM rocm/pytorch:latest

# For now install all python requirements in requirements folder
COPY requirements /requirements


# Set the default HSA version for 6700 XT
ENV HSA_OVERRIDE_GFX_VERSION="10.3.0"


RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    pylint

# Install python requirements
RUN pip install --upgrade pip && \ 
    for req in /requirements/*.txt; do pip install -r $req; done


# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh


