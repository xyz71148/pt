FROM sanfun/public:vpn-prod-v19
MAINTAINER Barry <dhole.me@gmail.com>

ENV VERSION 1.0.20

COPY docker-data/image /
COPY docker-data/supervisor /etc/supervisor/conf_d


RUN sh /bin/process_ssh.sh