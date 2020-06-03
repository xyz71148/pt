from flask import jsonify, Blueprint,current_app
from app.helpers.setting import Setting
import os

app = Blueprint('setting.constant', __name__)


@app.route('/api/constant', methods=['GET'])
def get_constant():
    """
    get constant
    ---
    tags:
     - front/setting
    responses:
     200:
       description: ok
    """
    constant = Setting.rows("constant")
    constant['port'] = os.getenv("PORT")
    constant['executor'] = os.getenv("EXECUTOR")
    constant['version'] = os.getenv("VERSION")
    constant['debug'] = current_app.config['DEBUG']

    return jsonify(constant)

