from flask import Blueprint, jsonify
from pt.libs.flask_jwt import get_access_token
from pt.libs.flask_jwt import jwt_required, current_identity
from .store_user import User

app = Blueprint('user', __name__)


@app.route('/api/me', methods=['get'])
@jwt_required()
def me():
    """
    me
    ---
    tags:
     - user
    security:
      - apiKeyAuth : []
    responses:
     200:
       description: ok
    """
    return jsonify({"code": 200, "msg": "", "body": User.toDict(current_identity)})


@app.route('/api/token/refresh', methods=['post'])
@jwt_required()
def token_refresh():
    """
    token_refresh
    ---
    tags:
     - user
    security:
      - apiKeyAuth : []
    responses:
     200:
       description: ok
    """
    access_token = get_access_token(current_identity)

    return jsonify({"code": 200, "msg": "验证成功", "body": {
        "user": {
            "level": current_identity.level,
        },
        "check_token_sec_gap": 2 * 60 * 60,
        "access_token": "JWT " + access_token
    }})

