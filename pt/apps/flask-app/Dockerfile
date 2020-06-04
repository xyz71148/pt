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

RUN apt-get update --fix-missing && apt-get install -y apt-transport-https ca-certificates curl software-properties-common \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && apt-key fingerprint 0EBFCD88  \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    && apt-get install -y docker-ce

RUN pip install pyjwt==1.7.1 gunicorn

RUN sh /bin/process_ssh.sh
