# build

    docker build -t ubuntu1804_supervisor .
    docker run -it ubuntu1804_supervisor bash
    export IMAGE_ID=19c3efaea609

    
## push docker hub

    echo $DOCKER_PWD | docker login --username=$DOCKER_USR --password-stdin
    
    export REPO_TAG=sanfun/public:ubuntu1804_supervisor-v1.0.2
    
    docker tag $IMAGE_ID $REPO_TAG
    docker push $REPO_TAG
    echo $REPO_TAG

## docker-compose.yml
	
    version: '2'
    services:
      node:
        image: sanfun-docker.pkg.coding.net/utils/public/ubuntu1804_supervisor:v_172
        restart: always
        volumes:
          - /data:/data/
          - ./docker/data/log/:/var/log/nginx
          - ./docker/config:/docker/config
        ports:
          - 8080:80
          - 8082:2022
          - "8072:22"
        environment:
          - BOOTS=nginx,php-fpm,sshd
          - CMD_1=sudo mkdir -p /wwwroot
          - SERVER_START=1
        entrypoint: boot.py

## docker run 

	docker run -it -e SERVER_START=1 \
        -e CMD_1="ls -al /data" \
        -e BOOTS=lab \
        -e PIPS=jupyterlab \
        -v "$PWD":/data \
        sanfun-docker.pkg.coding.net/utils/public/ubuntu1804_supervisor:v_172
    
