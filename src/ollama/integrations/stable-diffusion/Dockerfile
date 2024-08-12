FROM rocm/pytorch


WORKDIR /dockerx
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
WORKDIR /dockerx/stable-diffusion-webui


RUN python -m pip install --upgrade pip wheel && \
    pip install -r requirements.txt

# Install dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
    libgl1 \
    libglib2.0-0 \
    google-perftools 

ENV COMMANDLINE_ARGS=--skit-torch-cuda-test

# Expose the port
EXPOSE 8000


CMD [ "python3", "launch.py" ]