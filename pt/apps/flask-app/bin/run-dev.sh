#!/bin/bash
bash=$1

sudo docker build -f Dockerfile -t docker_dev .

sudo docker network create app || { echo "app network exists ";}
sudo docker rm -f docker_dev || { echo "error rm docker container";}

sudo docker run --name docker_dev \
    -e AP_ENV=1 \
    -e APP=sshd,app_dev \
    -e CMD_1='pip install -r requirements.txt' \
    -e AP_FLASK_ENV=dev \
    -e AP_PYTHONPATH=/data/home \
    -e AP_GOOGLE_APPLICATION_CREDENTIALS=/data/setting/credit.json.log \
    -p 9080:8080 \
    -p "8022:22" \
    -v $PWD:/data/home \
    -v $PWD/docker-data/setting:/data/setting \
    -v ~/data/root_cache:/root/.cache \
    --cap-add=NET_ADMIN \
    --network app \
    -it docker_dev $bash