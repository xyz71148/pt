import logging
import hashlib
import re
import subprocess
import os
from urllib.parse import urlparse, unquote, urlencode


def shell_exec_result(cmd, **e):
    env = dict(os.environ, **e)
    return subprocess.check_output(cmd, shell=True, env=env)


def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return bool(re.search(regex, email))


def md5(val_str):
    return hashlib.md5(val_str.encode()).hexdigest()


def set_logging_system_output(level=logging.INFO):
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(level)


def set_logging(level=logging.INFO):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(level)


def url_encode(dic):
    return urlencode(dic)


def url_decode_query(url):
    o = urlparse(url)
    j = dict()
    query = o.query
    for i in query.split("&"):
        t = i.split("=")
        j[t[0]] = unquote(t[1])
    return j