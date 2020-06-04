import flask
from pt.libs.flask_jwt import jwt_required, current_identity
from .store import Task as Model
import pt.libs.utils as utils

app = flask.Blueprint('admin.task', __name__)


@app.route('/api/admin/tasks', methods=['GET'])
@jwt_required()
def rows():
    """
    get tasks
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/task
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


@app.route('/api/admin/task/<task_id>', methods=['GET'])
@jwt_required()
def row(task_id):
    """
    get a task
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/task
    parameters:
      - name: task_id
        in: path
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = Model.get(task_id)
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": obj
    })


@app.route('/api/admin/task', methods=['POST'])
@jwt_required()
def post():
    """
    create a task
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/task
    parameters:
      - name: action
        default: shell
        in: formData
        required: true
      - name: params
        in: formData
        required: true
        default: export
        description:
            <p>curl https://{COMPUTE_PROJECT_ID}.appspot.com/f/p-gcp-deploy.sh | bash -s {BASIC_AUTH_USERNAME} {BASIC_AUTH_PASSWORD} {COMPUTE_PROJECT_ID} </p>
            <p>curl https://{COMPUTE_PROJECT_ID}.appspot.com/f/p-gcp-deploy.sh | bash -s {BASIC_AUTH_USERNAME} {BASIC_AUTH_PASSWORD} {COMPUTE_PROJECT_ID} </p>
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    try:
        json_data = flask.request.json.get("data", dict())
    except Exception as e:
        json_data = utils.http_post_decode(flask.request.data.decode("utf8"))

    obj = Model.create(json_data['data'])

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": obj
    })


@app.route('/api/admin/task/<task_id>', methods=['PUT'])
@jwt_required()
def save(task_id):
    """
    change a task
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/task
    parameters:
      - name: task_id
        in: path
        required: true
      - name: data
        in: formData
        required: true
      - name: executor
        in: formData
        required: true
      - name: status
        in: formData
        required: true
      - name: result
        in: formData
        required: true
    responses:
      200:
        description: ok
    """
    if current_identity.level != 0:
        return flask.jsonify({"code": 403, "body": []})
    obj = Model.row(task_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))
    try:
        json_data = flask.request.json.get("data", dict())
    except Exception as e:
        json_data = utils.http_post_decode(flask.request.data.decode("utf8"))

    for field in json_data.keys():
        setattr(obj, field, json_data[field])

    obj.save()
    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": obj.to_dict()
    })


@app.route('/api/admin/task/<task_id>/<action>', methods=['DELETE'])
@jwt_required()
def remove(task_id, action):
    """
    change a task
    ---
    security:
      - apiKeyAuth : []
    tags:
      - admin/task
    parameters:
      - name: task_id
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
    obj = Model.row(task_id)
    if obj is None:
        return flask.jsonify(dict(code=404, msg=""))

    if action == "remove":
        obj.remove()

    if action == "delete":
        obj.delete()

    return flask.jsonify({
        "code": 200,
        "msg": "",
        "body": None
    })

