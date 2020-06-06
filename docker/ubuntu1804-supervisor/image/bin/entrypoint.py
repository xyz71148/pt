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

if os.getenv("APPEND_ENV", None) is not None:
    os_system("rm -rf /etc/environment_")
    os_system("cat /etc/environment > /etc/environment_")
    if os.path.exists("/data/.environment"):
        os_system("cat /data/.environment >> /etc/environment_")

    for env_key in os.environ:
        if env_key.startswith("EXPORT_"):
            val = os.getenv(env_key, None)
            os_system("echo 'export {}={}' >> /etc/environment_".format(env_key, val))

    os_system("cat /etc/environment_ > /etc/environment")
    os_system("bash -c 'source /etc/environment'")

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


cmds = []
for env_key in os.environ:
    if env_key.startswith("CMD_"):
        index = env_key.replace("CMD_", "")
        cmd = os.getenv(env_key, None)
        logging.info("{},{}".format(index, cmd))
        cmds.append((int(index), cmd))

if len(cmds) > 0:
    cmds.sort(key=lambda k: k[0])
    logging.info(cmds)
    for (index, cmd) in cmds:
        logging.info("{0} > {1}".format(index, cmd))
        os_system(cmd)

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

BOOTS = os.getenv("BOOTS", None)
if BOOTS is not None:
    for item in BOOTS.split(","):
        if len(item) == 0:
            continue
        os_system("cp /etc/supervisor/conf_d/{0}.conf /etc/supervisor/conf.d/{0}.conf".format(item))

PIPS = os.getenv("PIPS", None)
if PIPS is not None:
    for item in PIPS.split(","):
        if len(item) == 0:
            continue
        os_system("pip install {}".format(item))

logging.info("starting")

if os.getenv("INIT_SCRIPT", None) is not None:
    os_system(os.getenv("INIT_SCRIPT", None))

os_system("mkdir -p /data/home /data/setting /data/log")

if os.getenv("SERVER_START", None) is not None:
    os_system("/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf")
else:
    if len(sys.argv) > 1:
        os_system(sys.argv[1])
    else:
        os_system("bash")
