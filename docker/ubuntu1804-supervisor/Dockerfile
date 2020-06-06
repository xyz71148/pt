FROM ubuntu:18.04
MAINTAINER Barry <dhole.me@gmail.com>

ENV TZ 'Asia/Shanghai'
ENV VERSION 1.0.11

RUN sed -i "s/security\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list && sed -i "s/archive\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list

RUN apt-get -y --fix-missing update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            net-tools  \
  			tzdata \
            inetutils-ping \
            supervisor \
            nginx \
            wget \
            curl \
            zip \
            unzip \
            vim \
            rsync \
            telnet \
            net-tools \
            cron \
            openssh-server \
            && service nginx stop \
            && service supervisor stop \
            && mkdir -p /var/run/sshd \
            && mkdir -p /root/.ssh \
            && touch /root/.ssh/authorized_keys \
  			&& echo $TZ > /etc/timezone \
  			&& rm /etc/localtime \
            && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
            && dpkg-reconfigure -f noninteractive tzdata 
  
COPY ./image/ /

RUN apt-get remove -y make && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/*

#ADD ./ /data/

USER root
#nginx
EXPOSE 80

#jupyter
EXPOSE 8020

WORKDIR /data

COPY ./init.py /bin/
COPY ./supervisor/ /etc/supervisor/conf_d/

RUN chmod +x /bin/init.py /bin/entrypoint.py

ENTRYPOINT ["/bin/entrypoint.py"]

CMD ["bash"]
