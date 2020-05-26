from flask import Blueprint, request
from app.helpers.auth import basic_auth
from ..var.store import Var

app = Blueprint('var.api', __name__)


@app.route('/f/<key>', methods=['GET'])
def file_get(key):
    """
    file get
    ---
    tags:
     - utils/var
    parameters:
      - name: key
        in: path
        required: true
    responses:
     200:
       description: ok
    """
    val = Var.get(key, is_json=False) if key[0:2] == "p-" else ""
    return val


@app.route('/s/<key>', methods=['GET'])
@basic_auth.login_required
def file_get_s(key):
    """
    secret file get
    ---
    tags:
     - utils/var
    parameters:
      - name: key
        in: path
        required: true
    responses:
     200:
       description: ok
    """
    return Var.get(key, is_json=False) if key[0:2] == "s-" else ""


@app.route('/api/upload/var/<key>', methods=['POST'])
@basic_auth.login_required
def upload_var(key):
    """
    upload_var
    ---
    tags:
     - utils/var
    parameters:
      - name: key
        in: path
        required: true
        description:   constant.json | setting.json
      - name: files
        in: formData
        type: file
        required: true
    responses:
     200:
       description: ok
    """
    file = request.files['files']
    val = file.read()
    if key in [
        "constant.json",
        "setting.json",
        "p-boot.py",
    ]:
        Var.del_cache(key)
        Var.set(key, val)
        return val
    else:
        raise Exception("key not in valid keys", 500)
