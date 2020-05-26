# from flask import request, jsonify, Blueprint
# from pt.libs.flask_jwt import jwt_required, current_identity
# from app.helpers.setting import Setting
#
# app = Blueprint('setting.admin', __name__)
#
#
# @app.route('/api/admin/setting/<namespace>/<key>', methods=['PUT'])
# @jwt_required()
# def setting_update(namespace, key):
#     """
#     settings set
#     ---
#     security:
#      - apiKeyAuth : []
#     tags:
#      - admin/setting
#     parameters:
#       - name: key
#         in: path
#         required: true
#       - name: namespace
#         in: path
#         default: setting
#         description: setting | constant
#         required: true
#       - name: body
#         in: body
#         description:
#         required: true
#         schema:
#           "$ref": "#/definitions/SettingRequest"
#     responses:
#      200:
#        description: ok
#     """
#     if current_identity.level != 0:
#         return jsonify({"code": 403, "body": []})
#     content = request.json
#     Setting.set(key, content['value'], namespace=namespace)
#     return jsonify({"code": 200, "body": content})
#
#
# @app.route('/api/admin/setting/<namespace>/<key>', methods=['DELETE'])
# @jwt_required()
# def setting_del(namespace, key):
#     """
#     settings set
#     ---
#     security:
#      - apiKeyAuth : []
#     tags:
#      - admin/setting
#     parameters:
#       - name: key
#         in: path
#         required: true
#       - name: namespace
#         in: path
#         default: setting
#         description: setting | constant
#         required: true
#     responses:
#      200:
#        description: ok
#     """
#     if current_identity.level != 0:
#         return jsonify({"code": 403, "body": []})
#     Setting.remove(key, namespace=namespace)
#     return jsonify({"code": 200, "body": ""})
#
#
# @app.route('/api/admin/settings/<namespace>', methods=['GET'])
# @jwt_required()
# def settings(namespace):
#     """
#     settings
#     ---
#     security:
#      - apiKeyAuth : []
#     tags:
#      - admin/setting
#     parameters:
#       - name: namespace
#         in: path
#         default: setting
#         description: setting | constant
#         required: true
#     responses:
#      200:
#        description: ok
#     """
#     if current_identity.level != 0:
#         return jsonify({"code": 403, "body": []})
#
#     rows = Setting.rows(namespace)
#     return jsonify({"code": 200, "body": [dict(
#         name=setting.name,
#         value=setting.value
#     ) for setting in rows]})
