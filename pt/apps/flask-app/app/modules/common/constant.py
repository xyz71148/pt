from flask import jsonify, Blueprint
from app.helpers.setting import Setting

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
    constant['network'] = Setting.get("NETWORK_INFURA", default="main")
    return jsonify(constant)

