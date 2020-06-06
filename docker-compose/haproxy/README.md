##


    git clone https://e.coding.net/sanfun/utils/pt-docker.git ~/pt-docker/
    cd ~/pt-docker
    git pull origin master
    
    cd ~/pt-docker/docker-compose/haproxy    
    git clone git@e.coding.net:sanfun/utils/docker-data.git    
    

    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    sudo docker-compose up


##common


    git add . && git commit -m "no msg" && git push origin master && \
    ssh dev "cd ~/pt-docker/docker-compose/haproxy/docker-data && git pull origin master"
    
    git add . && git commit -m "no msg" && git push origin master && \
    ssh dev "cd ~/pt-docker/ && git pull origin master"
    
    ssh dev "cd ~/pt-docker/docker-compose/haproxy && sudo docker-compose down"
    
    ssh dev "cd ~/pt-docker/docker-compose/haproxy && sudo docker-compose up -d"

    git clone https://e.coding.net/sanfun/utils/pt-docker.git ~/pt-docker/
    cd ~/pt-docker
    git pull origin master
    
    cd ~/pt-docker/docker-compose/haproxy    
    git clone git@e.coding.net:sanfun/utils/docker-data.git    
    
    sudo docker-compose restart
    sudo docker exec -it mock sh
    
    cd ~/pt-docker/docker-compose/haproxy/docker-data
    git pull origin master   
    
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    sudo docker-compose up
    sh ~/pt-docker/docker-compose/haproxy/bin/server.sh
    sh ~/pt-docker/docker-compose/haproxy/bin/cert.sh ws.jie8.cc
    
    ls ~/pt-docker/docker-compose/haproxy/certs

### haproxy 日志

    tail -f /var/log/syslog
    

	

	
