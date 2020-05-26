from flask import request
from random import Random,SystemRandom
import hashlib


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