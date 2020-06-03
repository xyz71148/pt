FROM sanfun/public:worker-v1
MAINTAINER Barry <dhole.me@gmail.com>

ENV VERSION 1.0.2
ENV GOOGLE_APPLICATION_CREDENTIALS /opt/worker/account.json
ENV PORT 9090
ENV IP 0.0.0.0
ENV EXECUTOR docker

COPY docker-data/image /
COPY docker-data/supervisor /etc/supervisor/conf_d
COPY ./ /data/home

#
RUN pip install pyjwt==1.7.1 gunicorn


RUN sh /bin/process_ssh.sh