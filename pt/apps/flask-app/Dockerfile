FROM sanfun/public:vpn-prod-v19
MAINTAINER Barry <dhole.me@gmail.com>

ENV VERSION 1.0.1
ENV GOOGLE_APPLICATION_CREDENTIALS /opt/worker/account.json
ENV PORT 8080
ENV IP 0.0.0.0
ENV EXECUTOR docker

COPY docker-data/image /
COPY docker-data/supervisor /etc/supervisor/conf_d

RUN pip install simplejson \
        requests \
        google-cloud-ndb \
        web3 \
        jwt \
        paypalrestsdk \
        websockets \
        flask \
        flask_socketio \
        sqlalchemy \
        flask_sqlalchemy \
        flask_bootstrap \
        flask_cors \
        flask_swagger \
        flask_caching \
        pyjwt \
        google-api-python-client \
        git+https://github.com/xyz71148/pt

RUN sh /bin/process_ssh.sh