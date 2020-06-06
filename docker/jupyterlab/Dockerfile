FROM sanfun-docker.pkg.coding.net/utils/public/ubuntu1804_supervisor:v_172

MAINTAINER Barry <dhole.me@gmail.com>
ENV VERSION 1.0.6

RUN apt-get -y --fix-missing update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            python3-setuptools \
            python3 \
            python3-pip \
            && ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install jupyterlab pandas numpy scipy matplotlib

RUN apt-get remove -y make && apt-get autoremove -y \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/*

WORKDIR /data

#jupyter
EXPOSE 8020
