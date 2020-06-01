import logging
import hashlib
import re
import subprocess
import os
from flask import request
from random import Random,SystemRandom
from urllib.parse import urlparse, unquote, urlencode


def shell_exec_result(cmd, **e):
    env = dict(os.environ, **e)
    try:
        return subprocess.check_output(cmd, shell=True, env=env,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = "command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output)
        raise RuntimeError(msg)


def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return bool(re.search(regex, email))



def md5(val_str):
    return hashlib.md5(val_str.encode()).hexdigest()


def generate_random(len):
    try:
        random = SystemRandom()
        random.random()
    except NotImplementedError:  # pragma: no cover
        random = Random()
    return md5(str(random.random()))[0:len]


def get_base_url():
    try:
        x_host = request.headers.get("X-Forwarded-Host", None)
        host = request.host
        # print(request.headers)
        # print("X-Forwarded-Host", x_host, host)
        scheme = request.scheme
        if x_host is not None and request.host != x_host:
            host = x_host
            scheme = "http"
        return "{}://{}".format(scheme, host)
    except Exception as e:
        print(e)
        return ""


def set_logging_system_output(level=logging.INFO):
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(level)


def set_logging_file(level,path):
    logFormatter = logging.Formatter('[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                                 '%m-%d %H:%M:%S')
    fh = logging.FileHandler(path)
    fh.setFormatter(logFormatter)

    if level == "debug":
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(fh)


def set_logging(level=logging.INFO):
    logFormatter = logging.Formatter('[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                                 '%m-%d %H:%M:%S')
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(level)


def url_encode(dic):
    return urlencode(dic)


def http_post_decode(data):
    j = dict()
    for i in data.split("&"):
        t = i.split("=")
        j[t[0]] = unquote(t[1])
    return j


def url_decode_query(url):
    o = urlparse(url)
    j = dict()
    query = o.query
    for i in query.split("&"):
        t = i.split("=")
        j[t[0]] = unquote(t[1])
    return j


def get_host_ip():
    ip = shell_exec_result("dig +short myip.opendns.com @resolver1.opendns.com")
    return ip.decode("utf8").strip()


def file_write(path,content):
    f = open(path, "w")
    f.write(content)
    f.close()


def file_read(path):
    f = open(path, "r")
    content = f.read().strip()
    f.close()
    return content
