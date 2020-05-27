from flask_caching import Cache

cache = Cache(config={
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "./.cache",
    "CACHE_DEFAULT_TIMEOUT": 300
})


def mail_send(email, title, content):
    pass
