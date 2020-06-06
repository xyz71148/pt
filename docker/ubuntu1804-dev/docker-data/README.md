# build
    
    docker build -t dev -f Dockerfile.py27.gcloud .
    docker network create app
    docker run --rm --name dev -v $PWD:/data/home -p 5000:5000 --network app -it dev bash
    docker container inspect dev
    
    export IMAGE_NAME=sanfun-docker.pkg.coding.net/utils/public/ubuntu1804-dev:py27-v1
    export IMAGE_NAME=sanfun/public:ubuntu1804-dev-py27-v1
    sudo docker tag dev:latest $IMAGE_NAME
    sudo echo $DOCKER_PWD | sudo docker login  --username=$DOCKER_USR --password-stdin docker.io
    sudo docker push $IMAGE_NAME
    

# Dockerfile

    FROM sanfun/public:ubuntu1804-dev-py27-v01
    MAINTAINER Barry <dhole.me@gmail.com>
    ENV VERSION 1.0.0
    RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                make
    #flask
    EXPOSE 5000
    WORKDIR /data/home
    CMD ["bash"]
