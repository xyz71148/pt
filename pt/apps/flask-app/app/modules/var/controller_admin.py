import flask
from pt.libs.flask_jwt import jwt_required, current_identity
from .store import Var

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
    page = flask.request.args.get('page', "1")
    limit = flask.request.args.get('limit', "10")
    order = flask.request.args.get('order', "-created_at")
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Var.rows(page=page, limit=limit,order=order)
    })


@app.route('/api/admin/var/fields', methods=['GET'])
@jwt_required()
def fields():
    """
    get var fields
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Var.get_fields()
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
    obj = Var.row(var_id)

    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))
    body = Var.get_detail(obj)
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
    items = json_data['address'].split("\n")
    obj = Var()
    addresses = Var.addresses()
    rows = []
    for address in items:
        if len(address) > 0 and address not in addresses:
            obj.address = address
            obj.put()
            rows.append(address)

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": rows
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
    obj = Var.row(var_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    json_data = flask.request.json.get("data", dict())

    for field in json_data.keys():
        if field == "used":
            value = True if json_data[field] == "true" else False
        else:
            value = json_data[field]
        setattr(obj, field, value)

    obj.put()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": Var.get_detail(obj)
    })


@app.route('/api/admin/var/<var_id>', methods=['DELETE'])
@jwt_required()
def remove(var_id):
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
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = Var.row(var_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))
    obj.is_deleted = True
    obj.put()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": None
    })
