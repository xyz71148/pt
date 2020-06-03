import flask
import simplejson as json
import requests
from app.helpers.setting import Setting
from .store import Task as Model
from pt.libs.utils import set_logging
import logging
import os

set_logging()


app = flask.Blueprint('tasks', __name__)


@app.route('/api/task/handler', methods=['POST'])
def task_handler():
    """
    task handler
    ---
    tags:
     - task
    security:
      - apiKeyAuth : []
    responses:
     200:
       description: ok
    """
    payload = flask.request.get_data(as_text=True) or '(empty payload)'
    logging.info('Received task with payload: {}'.format(payload))
    payload = json.loads(str(payload))

    task_id = payload['task_id']
    auth = payload['auth']
    if Setting.get("TASK_AUTH", default="TASK_AUTH_KEY", update=True) != auth:
        logging.error("TASK_AUTH is invalid")
        raise Exception("auth is invalid", 500)
    status, result = Model.exec(payload['action'], payload['params'])
    logging.info("exe result: %s %s", status, result)
    res = requests.post("https://{}.appspot.com/api/task/result/{}".format(Setting.get("COMPUTE_PROJECT_ID"), task_id), data=dict(
        status=status,
        result=result,
        executor=os.getenv("EXECUTOR", "docker")
    ))
    logging.info("upload response code: %d", res.status_code)
    return status
