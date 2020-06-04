

    export IMAGE_NAME=sanfun/public:worker-v12
    sudo docker tag docker_dev $IMAGE_NAME
    echo $DOCKER_PWD | sudo docker login --username $DOCKER_USR --password-stdin
    sudo docker push $IMAGE_NAME
