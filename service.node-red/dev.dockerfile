FROM nodered/node-red-docker

USER root
# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip
RUN apt-get update || : && apt-get install python3 -y

USER '0'
COPY ./service.node-red/app /app

COPY ./service.node-red/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN npm install -g node-red-contrib-python3-function
# RUN npm install node-red -g
RUN npm i node-red-contrib-web-worldmap -g


