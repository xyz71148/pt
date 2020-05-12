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
    
    python setup.py check
    python setup.py sdist bdist_wheel
    twine upload --repository-url testpypi dist/*
    python setup.py upload

## init gcp template

    sudo apt-get install -y python3-pip
    sudo pip3 install git+https://github.com/xyz71148/pt
    sudo pt -m server.ubuntu.init_docker