import flask
from pt.libs.flask_jwt import jwt_required, current_identity
from .store import Var as Model

app = flask.Blueprint('admin.var', __name__)


@app.route('/api/admin/vars', methods=['GET'])
@jwt_required()
def rows():
    """
    get vars
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
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


@app.route('/api/admin/var/<var_id>', methods=['GET'])
@jwt_required()
def row(var_id):
    """
    get a var
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
    parameters:
      - name: var_id
        in: path
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = Model.row(var_id)

    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))
    body = Model.to_dict(obj)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": body
    })


@app.route('/api/admin/var', methods=['POST'])
@jwt_required()
def post():
    """
    create a var
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
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
        setattr(obj, field, json_data[field])

    obj = Model.put(obj)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Model.to_dict(obj)
    })


@app.route('/api/admin/var/<var_id>', methods=['PUT'])
@jwt_required()
def put(var_id):
    """
    change a var
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
    parameters:
      - name: var_id
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
    obj = Model.row(var_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    json_data = flask.request.json.get("data", dict())

    for field in json_data.keys():
        setattr(obj, field, json_data[field])
    obj = Model.put(obj)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Model.to_dict(obj)
    })


@app.route('/api/admin/var/<var_id>/<action>', methods=['DELETE'])
@jwt_required()
def remove(var_id, action):
    """
    change a var
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
    parameters:
      - name: var_id
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
    obj = Model.row(var_id)
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
