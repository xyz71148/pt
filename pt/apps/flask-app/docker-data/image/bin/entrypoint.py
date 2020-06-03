#!/usr/bin/env python
import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s : %(message)s')


def os_system(cmd, info=1):
    cmd = cmd.strip('"').strip(",")
    msg = "> exec: {}".format(cmd)
    if info == 1:
        logging.info(msg)
    error = os.system(cmd)
    if error > 0:
        logging.info("run result: {}".format(error))
        sys.exit(1)


if os.getenv("AP_ENV", None) is not None:
    os_system("bash -c 'touch /etc/profile.d/env.sh'")
    for env_key in os.environ:
        if env_key.startswith("AP_"):
            val = os.getenv(env_key, None)
            os_system("echo 'export {}={}' >> /etc/profile.d/env.sh".format(env_key[3:], val))
            os_system("echo '{}={}' >> /root/.ssh/environment".format(env_key[3:], val))

    os_system("bash -c 'source /etc/profile.d/env.sh'")


def do_init_user():
    id = 1201
    for env_key in os.environ:
        if env_key.startswith("PK_"):
            key = env_key.replace("PK_", "")
            t = key.split("_")
            username = t[0]
            public_key = os.getenv(env_key, None)
            logging.info(">> do_init_user: {0}@{1}".format(username, public_key))
            if public_key is None:
                continue
            if username == "root":
                os_system("echo {0} >> /root/.ssh/authorized_keys".format(public_key))
            else:
                id += 1
                os_system("useradd --uid {0} --gid www --shell /bin/bash --create-home {1}".format(id, username))
                os_system("echo '{0}:{0}_2018' | chpasswd".format(username))
                os_system("su - {} -c 'id'".format(username))
                os_system("su - {} -c 'mkdir -p ~/.ssh'".format(username))
                os_system("su - {0} -c 'echo {1} >> ~/.ssh/authorized_keys'".format(username, public_key))
                os_system("su - {0} -c 'chmod 600 ~/.ssh/authorized_keys'".format(username))
            os_system("chmod 600 /root/.ssh/authorized_keys")


def handle_alias():
    os_system("touch ~/.bash_aliases")
    rows = []
    for env_key in os.environ:
        if env_key.startswith("ALIAS_"):
            index = env_key.replace("ALIAS_", "")
            cmd = os.getenv(env_key, None)
            logging.info("{},{}".format(index, cmd))
            rows.append((index, cmd))

    if len(rows) > 0:
        logging.info(rows)
        for (key, row) in rows:
            logging.info("{0} > {1}".format(key, row))
            os_system("echo \"alias {}='{}'\" >> ~/.bash_aliases".format(key, row))


def handle_cmd():
    rows = []
    for env_key in os.environ:
        if env_key.startswith("CMD_"):
            index = env_key.replace("CMD_", "")
            cmd = os.getenv(env_key, None)
            logging.info("{},{}".format(index, cmd))
            rows.append((int(index), cmd))

    if len(rows) > 0:
        rows.sort(key=lambda k: k[0])
        logging.info(rows)
        for (index, row) in rows:
            logging.info("{0} > {1}".format(index, row))
            os_system(row)


handle_cmd()
handle_alias()
os_system("cat ~/.bash_aliases")

for env_key in os.environ:
    if env_key.startswith("AU_"):
        key = env_key.replace("AU_", "")
        t = key.split("_")
        username = t[0]
        password = os.getenv(env_key, None)
        logging.info(">> htpasswd: {0}@{1}".format(username, password))
        if password is not None:
            os_system("touch {2} && chmod 777 {2} && echo {0}:{1} >> {2}".format(username, password,
                                                                                 "/etc/nginx/.htpasswd"))
do_init_user()

APP = os.getenv("APP", None)
if APP is not None:
    for item in APP.split(","):
        if len(item) == 0:
            continue
        os_system("cp /etc/supervisor/conf_d/{0}.conf /etc/supervisor/conf.d/{0}.conf".format(item))

PIP = os.getenv("PIP", None)
if PIP is not None:
    for item in PIP.split(","):
        if len(item) == 0:
            continue
        os_system("pip install {}".format(item))

PIP3 = os.getenv("PIP3", None)
if PIP3 is not None:
    for item in PIP3.split(","):
        if len(item) == 0:
            continue
        os_system("pip3 install {}".format(item))

logging.info("starting")

if os.getenv("INIT_PY", None) is not None:
    os_system(os.getenv("INIT_PY", None))

os_system("mkdir -p /data/home /data/setting /data/log /data/opt")
logging.info(sys.argv)

if len(sys.argv) == 2 and sys.argv[1] == "supervisord":
    os_system("/usr/local/bin/supervisord -n -c /etc/supervisor/supervisord.conf")
else:
    os_system(sys.argv[1])
