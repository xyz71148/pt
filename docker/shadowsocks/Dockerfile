FROM sanfun-docker.pkg.coding.net/utils/public/ubuntu1804_supervisor:v_172
MAINTAINER Barry <dhole.me@gmail.com>
ENV VERSION 1.0.8

COPY ./image/ /

RUN apt-get -y --fix-missing update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            python3-setuptools \
            python3 \
            python3-pip \
            iptables \
            gcc automake make build-essential\
            && ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install shadowsocks==2.8.2

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf \
    && echo "nameserver 8.8.4.4" >> /etc/resolv.conf

RUN cd /root \
        #&& wget --no-check-certificate -O libsodium-1.0.10.tar.gz https://github.com/jedisct1/libsodium/releases/download/1.0.10/libsodium-1.0.10.tar.gz \
        && tar -xf libsodium-1.0.10.tar.gz && cd libsodium-1.0.10 \
        && ./configure && make && make install \
        && echo "/usr/local/lib" > /etc/ld.so.conf.d/local.conf && ldconfig \
        && cd ../ && rm -rf libsodium*
RUN sed -i 's/cleanup/reset/g' /usr/local/lib/python3.6/dist-packages/shadowsocks/crypto/openssl.py
RUN apt-get remove -y make && apt-get autoremove -y \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/*

WORKDIR /data

#jupyter
EXPOSE 8082

#shadowsocks
EXPOSE 8071