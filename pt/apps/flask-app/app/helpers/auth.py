import flask
from pt.libs.flask_httpauth.flask_httpauth import HTTPBasicAuth
from .setting import Setting

basic_auth = HTTPBasicAuth()


def get_basic_auth():
    global basic_auth
    return basic_auth


@basic_auth.get_password
def get_password(username):
    if username == Setting.get("BASIC_AUTH_USERNAME", default="admin", update=True):
        return Setting.get("BASIC_AUTH_PASSWORD", default="admin888", update=True)
    if username == Setting.get("BASIC_AUTH_USERNAME_1", default="user", update=True):
        return Setting.get("BASIC_AUTH_PASSWORD_1", default="user888", update=True)
    if username == Setting.get("BASIC_AUTH_USER_NAME_STARTUP_SERVER", default="user", update=True):
        return Setting.get("BASIC_AUTH_PASSWORD_STARTUP_SERVER", default="user888", update=True)
    return None


@basic_auth.error_handler
def unauthorized():
    return flask.make_response(flask.jsonify({'error': 'Unauthorized access'}), 401)

