- https://meetrix.io/blog/webrtc/turnserver/long_term_cred.html

www

    git_repo=https://e.coding.net/sanfun/utils/pt-docker.git
    ssh dev "curl https://jie8.cc/f/p-build | bash -s $git_repo /docker/turnserver turnserver-v1 $DOCKER_USR $DOCKER_PWD"   

    sudo docker run -it sanfun/public:turnserver-v1 bash

    git clone $git_repo

    sudo docker rm -f my-coturn
    sudo docker run -d --net=host -e TURN_SECRET=TURN_SECRET_2020  -e TURN_PORT=8478 --name my-coturn -t coturn-long-term-cred

    sudo docker run -d --net=host \
        -e TURN_SECRET=TURN_SECRET_2020  \
        -e TURN_PORT=8478 sanfun/public:turnserver-v1

# gen secret

    secret=mysecret && \
    time=$(date +%s) && \
    expiry=8400 && \
    username=$(( $time + $expiry )) &&\
    echo username:$username && \
    echo password : $(echo -n $username | openssl dgst -binary -sha1 -hmac $secret | openssl base64)
    