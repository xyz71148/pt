import flask
import logging
import requests
import os
from app.helpers.setting import Setting
from app.modules.var.store import Var
import pt.libs.utils as utils

app = flask.Blueprint('common', __name__)


@app.route('/err', methods=['GET'])
def err():
    logging.info("==>>info")
    logging.debug("==>>debug")
    raise Exception("error", 505)


@app.route('/check', methods=['GET'])
def check():
    logging.info("checking...")
    if not Setting.get("INITED", default=False):
        if os.path.exists("/opt/worker/setting.json"):
            logging.info("init setting.json")
            Var.set("setting.json", utils.file_read("/opt/worker/setting.json"))
            Setting.set("INITED", True)

    url = "https://{}.appspot.com/api/compute/instance/worker/{}".format(
        Setting.get("COMPUTE_PROJECT_ID"),
        os.getenv("EXECUTOR", "docker").split("|")[0]
    )
    logging.info("upload worker status... %s",url)

    res = requests.post(url, data=dict(
        ip=os.getenv("IP"),
        port=os.getenv("PORT")
    ), auth=(Setting.get("BASIC_AUTH_USERNAME"), Setting.get("BASIC_AUTH_PASSWORD")))
    logging.info("res: %s",res)
    return "ok"


@app.route('/', methods=['GET'])
def index():
    return "hi"
    # return flask.render_template('index.html')
