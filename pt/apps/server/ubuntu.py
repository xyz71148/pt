import pt.libs.utils as utils

cmd = """
echo "ubuntu 18.04 init..."
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install -y curl git expect docker-ce docker-ce-cli containerd.io

# Make sure docker service is running
sudo service docker start

sudo docker pull sanfun/public:shadowsocks-v1 busybox kylemanna/openvpn
# Test docker installation
sudo docker ps
"""


def init_docker():
    utils.shell_exec_result(cmd)


def add_docker_group():
    utils.shell_exec_result("""sudo usermod -aG docker $USER && sudo newgrp docker""")