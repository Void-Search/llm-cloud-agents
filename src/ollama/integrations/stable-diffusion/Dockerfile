FROM python:3.10.14-bullseye
# Install dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
    libgl1 \
    libglib2.0-0 \
    google-perftools 

# Create a new user and switch to that user
RUN useradd -m stable-diffusion
USER stable-diffusion
WORKDIR /home/stable-diffusion/
# Install the stable diffusion code
RUN wget https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh

RUN chmod +x ./webui.sh && ./webui.sh 
WORKDIR /home/stable-diffusion/stable-diffusion-webui
RUN python -m pip install --upgrade pip wheel
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000


CMD [ "python3", "launch.py" ]