import flask
from pt.libs.utils import md5
from pt.libs.flask_jwt import jwt_required, current_identity

from .store_user import User as Model

app = flask.Blueprint('admin.user', __name__)


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
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Model.rows(**flask.request.args)
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
    obj = Model.row(user_id)

    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))
    body = Model.to_dict(obj)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": body
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

    obj = Model()

    for field in json_data.keys():
        if field == "password":
            json_data[field] = md5(json_data[field])
        setattr(obj, field, json_data[field])

    obj = Model.put(obj)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Model.to_dict(obj)
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
    obj = Model.row(user_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    json_data = flask.request.json.get("data", dict())

    for field in json_data.keys():
        if field == "password":
            json_data[field] = md5(json_data[field])
        setattr(obj, field, json_data[field])
    obj = Model.put(obj)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Model.to_dict(obj)
    })


@app.route('/api/admin/user/<user_id>/<action>', methods=['DELETE'])
@jwt_required()
def remove(user_id, action):
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
      - name: action
        in: path
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = Model.row(user_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    if action == "remove":
        Model.remove(obj)

    if action == "delete":
        Model.delete(obj)

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": None
    })
