- https://meetrix.io/blog/webrtc/turnserver/long_term_cred.html

    TAG_NAME=nginx-php7-alpine-v12
    git_repo=https://e.coding.net/sanfun/utils/pt-docker.git
    ssh dev "curl https://jie8.cc/f/p-build | bash -s $git_repo /docker/nginx-php7-alpine $TAG_NAME $DOCKER_USR $DOCKER_PWD"   
    
    sudo docker run -it sanfun/public:$TAG_NAME bash
    