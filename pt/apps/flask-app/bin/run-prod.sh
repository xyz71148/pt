sudo docker build -f Dockerfile.prod -t vpn_docker_prod .
sudo docker rm -f vpn_docker_prod && \
sudo docker run -d --name vpn_docker_prod \
    -e APP=sshd,app_1 \
    -v $PWD/docker-data/setting:/data/setting \
    -v $PWD/docker-data/logs:/data/logs \
    -p "8023:22" \
    --cap-add=NET_ADMIN \
    --network app -it \
    sanfun/public:vpn-prod-v17

sudo docker exec -it vpn_docker_prod bash