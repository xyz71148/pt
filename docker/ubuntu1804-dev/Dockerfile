FROM sanfun/public:ubuntu1804-dev-py27-v1
MAINTAINER Barry <dhole.me@gmail.com>

ENV TZ 'Asia/Shanghai'
ENV VERSION 1.0.11

#RUN sed -i "s/security\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list && sed -i "s/archive\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list
#RUN sed -i "s/mirrors\.ustc\.edu\.cn/security\.ubuntu\.com/g" /etc/apt/*.list && sed -i "s/archive\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list
RUN sed -i "s/mirrors\.ustc\.edu\.cn/mirrors\.aliyun\.com/g" /etc/apt/*.list && sed -i "s/archive\.ubuntu\.com/mirrors\.ustc\.edu\.cn/g" /etc/apt/*.list

COPY docker-data/image /

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            make
#flask
EXPOSE 5000
WORKDIR /data/hme
CMD ["bash"]
