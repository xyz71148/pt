#!/bin/bash
bash=$1

sudo docker build -f Dockerfile -t docker_dev .

sudo docker rm -f docker_dev || { echo "error rm docker container";}

sudo docker run --name docker_dev \
    -e APP=check,app_prod \
    -e FLASK_ENV=dev \
    -e PYTHONPATH=/data/home \
    -e PORT=9090 \
    -e IP=0.0.0.0 \
    -e EXECUTOR=docker \
    -e GOOGLE_APPLICATION_CREDENTIALS=/opt/worker/credit.json.log \
    -p 9090:9090 \
    -v $PWD:/data/home \
    -v $PWD/docker-data/setting:/opt/worker \
    -it docker_dev $bash