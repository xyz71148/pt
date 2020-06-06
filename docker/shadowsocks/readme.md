## docker

cmd
    
    export TAG_NAME=shadowsocks
    sudo docker build -t $TAG_NAME .
    sudo docker run -it -e SERVER_START=1 \
          -e CMD_1="ls  /etc/supervisor/conf_d/" \
          -e SS_PORT=8071 \
          -e SS_HOST=0.0.0.0 \
          -e SS_M=aes-256-cfb \
          -e SS_PWD=test111 \
          -e BOOTS=ss \
          -p 8071:8071 \
          --cap-add=NET_ADMIN \
          --rm --name shadowsocks \
          sanfun-docker.pkg.coding.net/utils/public/shadowsocks:v_173

          
     sudo docker exec -it shadowsocks bash
     
     
push dockerhub

    export IMAGE_NAME=sanfun/public:shadowsocks-v1
    sudo docker tag sanfun-docker.pkg.coding.net/utils/public/shadowsocks:v_173 $IMAGE_NAME
    sudo echo $DOCKER_PWD | docker login --username=$DOCKER_USR --password-stdin
    sudo docker push $IMAGE_NAME

## IPTABLES

- https://la4ji.blogspot.com/2017/08/shadowsocks.html

限制SS访问youtube.com

    -A
     # 添加iptables规则；
     -D
     # 删除iptables规则（把添加防火墙规则时代码中的 -A 改成 -D 即可删除添加的规则）；
     -m string
     # 指定模块；
     --string "youtube.com"
     # 指定要匹配的字符串(域名、关键词等)；
     --algo bm
     # 指定匹配字符串模式/算法（还有一种更复杂的算法：kmp）；
     --to 65535
     # 指定端口，这里代表所有端口（1-65535）；
     -j DROP
     # 指匹配到数据包后处理方式，这里是丢弃数据包。
     
    #添加
    iptables -A OUTPUT -m string --string "facebook.com" --algo kmp -j DROP
    #删除
    iptables -D OUTPUT -m string --string "facebook.com" --algo kmp -j DROP
    
    iptables -t filter -A FORWARD -p udp -m string --algo bm --string facebook.com -j ACCEPT
    iptables -t filter -A FORWARD -p udp -m string --algo bm --string google.com -j ACCEPT

    #全部清除
    iptables -P INPUT ACCEPT
    iptables -F
    iptables -L
    iptables -L -n -v
