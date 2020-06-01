import flask
from pt.libs.flask_jwt import jwt_required, current_identity
import simplejson as json
from .store import Var as Model
import mimetypes
import time

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
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": obj.to_dict()
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

    obj.versions = "{}"
    obj.save()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": obj.to_dict()
    })


@app.route('/api/admin/var/<var_id>', methods=['PUT'])
@jwt_required()
def save(var_id):
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
        if field == 'value':
            if "versions" in vars(obj).keys():
                versions = json.loads(obj.versions)
            else:
                versions = dict()
            versions[int(time.time())] = json_data[field]
            obj.versions = json.dumps(versions)

    obj.save()
    obj.del_cache()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": obj.to_dict()
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

    obj.del_cache()

    if action == "remove":
        obj.remove()

    if action == "delete":
        obj.delete()

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": None
    })


@app.route('/api/admin/var/export', methods=['GET'])
@jwt_required()
def export():
    """
    export
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

    data = Model.rows(limit=-1)

    if data is None:
        return flask.jsonify(dict(code=404, msg=""))

    file_name = "vars.json"
    response = flask.make_response(json.dumps(data["rows"]))
    mime_type = mimetypes.guess_type(file_name)[0]
    response.headers['Content-Type'] = mime_type
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
    return response


@app.route('/api/admin/var/import', methods=['POST'])
@jwt_required()
def post_import():
    """
    post_import
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/var
    parameters:
      - name: files
        in: formData
        type: file
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    file = flask.request.files['files']
    val = file.read()
    try:
        json_data = json.loads(val)
    except Exception as e:
        raise e
    if str(type(json_data)) != "<class 'list'>":
        Model.set(json_data['name'], json_data['value'])
    else:
        for row in json_data:
            Model.set(row['name'], row['value'])

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": ""
    })
