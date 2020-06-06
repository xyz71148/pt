FROM ubuntu:16.04
MAINTAINER Buddhika Jayawardhana <jay@meetrix.io>

ENV VERSION 1.0.3

RUN sed -i "s/security\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list && sed -i "s/archive\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list

RUN apt-get update && apt-get install -y coturn && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV TURN_PORT 3478
ENV TURN_PORT_START 10000
ENV TURN_PORT_END 20000
ENV TURN_SECRET mysecret
ENV TURN_SERVER_NAME coturn
ENV TURN_REALM north.gov

ADD start.sh start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]