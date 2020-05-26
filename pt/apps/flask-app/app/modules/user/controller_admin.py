import flask
from pt.libs.flask_jwt import jwt_required, current_identity
from pt.libs.utils import md5
from .store_user import User

app = flask.Blueprint('admin.user.admin', __name__)


@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def rows():
    """
    get users
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    parameters:
      - name: page
        in: query
        default: 1
        required: true
      - name: limit
        in: query
        default: 10
        required: true
      - name: order
        in: query
        default: -created_at
        required: true
    responses:
      200:
        description: ok
    """

    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    page = flask.request.args.get('page', "1")
    limit = flask.request.args.get('limit', "10")
    order = flask.request.args.get('order', "-created_at")

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": User.rows(page=page, limit=limit, order=order)
    })


@app.route('/api/admin/user/fields', methods=['GET'])
@jwt_required()
def fields():
    """
    get user fields
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": User.get_fields()
    })


@app.route('/api/admin/user/<user_id>', methods=['GET'])
@jwt_required()
def row(user_id):
    """
    get a user
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    parameters:
      - name: user_id
        in: path
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = User.row(user_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    body = User.get_detail(obj)

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": body
    })


@app.route('/api/admin/user/checkout/<user_id>/<flag>', methods=['GET'])
@jwt_required()
def rows_checkout(user_id, flag):
    """
    checkout
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    parameters:
      - name: user_id
        in: path
        required: true
      - name: flag
        in: path
        required: true
        description: gold | silver | copper
      - name: page
        in: query
        default: 1
        required: true
      - name: limit
        in: query
        default: 10
        required: true
      - name: order
        in: query
        default: -created_at
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})

    page = flask.request.args.get('page', "1")
    limit = flask.request.args.get('limit', "10")
    order = flask.request.args.get('order', "-created_at")

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": CheckOut.rows_by_user_id_flag(user_id, flag, page=page, limit=limit, order=order)
    })


@app.route('/api/admin/user', methods=['POST'])
@jwt_required()
def post():
    """
    create a user
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    parameters:
      - name: body
        in: body
        description:
        required: true
        schema:
          "$ref": "#/definitions/JsonRequest"
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})

    json_data = flask.request.json.get("data", dict())

    obj = User()
    for field in json_data.keys():
        value = json_data[field]
        setattr(obj, field, value)
    obj.put()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": User.get_detail(obj)
    })


@app.route('/api/admin/user/<user_id>', methods=['PUT'])
@jwt_required()
def put(user_id):
    """
    change a user
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    parameters:
      - name: user_id
        in: path
        required: true
      - name: body
        in: body
        description:
        required: true
        schema:
          "$ref": "#/definitions/JsonRequest"
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = User.row(user_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    json_data = flask.request.json.get("data", dict())

    for field in json_data.keys():
        value = json_data[field]
        if field == "level":
            value = int(value)
        if field == "password":
            value = md5(value)
        if field in ["balance_gold", "balance_copper", "balance_silver"]:
            value = float(value)
        setattr(obj, field, value)
    obj.put()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": User.get_detail(obj)
    })


@app.route('/api/admin/user/<user_id>', methods=['DELETE'])
@jwt_required()
def remove(user_id):
    """
    change a user
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/user
    parameters:
      - name: user_id
        in: path
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = User.row(user_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))
    obj.is_deleted = True
    obj.put()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": None
    })
