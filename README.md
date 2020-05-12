Pt
==============

[![Build Status](https://travis-ci.org/xyz71148/pt.png?branch=master)](https://travis-ci.org/xyz71148/pt)



Installation
------------


You can install this package as usual with pip:

    
    git add . && git commit -m "no msg" && git push origin master && \
    sudo pip3 install git+https://github.com/xyz71148/pt
    
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    python setup.py register
    python setup.py check
    python setup.py sdist
    python setup.py upload
    python setup.py register sdist upload

## init gcp template

    sudo apt-get install -y python3-pip
    sudo pip3 install git+https://github.com/xyz71148/pt
    sudo pt -m server.ubuntu.init_docker
    
    
    alias vpn='cd ~/data/bin && chmod +x y-deng.darwin.amd64.v1.0 && sudo ./y-deng.darwin.amd64.v1.0'
    alias oss='curl http://jie8.cc/f/p-oss'
