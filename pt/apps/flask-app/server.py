import os
import logging
from optparse import OptionParser
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_swagger import swagger
from pt.libs.flask_jwt import JWT
from app.helpers.helper import cache
from app.helpers.auth import basic_auth
from app.helpers.pt_exception import JSONExceptionHandler
from app.modules.user.store_user import User
from app.helpers.setting import Setting
from app.helpers import database
from app.modules import router
from app.modules.common.swagger import get_spec
from pt.libs.utils import set_logging_file, set_logging, md5

app = Flask(__name__)


@app.route("/api/spec")
@basic_auth.login_required
def spec():
    if Setting.get("DISABLE_SWAGGER", default="false", update=True) == "true":
        raise Exception("DISABLED", 403)
    swag = get_spec(swagger(app))
    return jsonify(swag)


def authenticate():
    pass


def identity(payload):
    user_id = payload['identity']
    return User.row(int(user_id))


parser = OptionParser()
parser.add_option("-p", "--port", default="9090", dest="port", help="server port listen on")
parser.add_option("-i", "--ip", default="0.0.0.0", dest="ip", help="server ip listen on")
parser.add_option("-f", "--log_file", default="./app.log", dest="log_file", help="location of log file")

# mysql://root:password@127.0.0.1:3306/test
parser.add_option("-d", "--dsn", default="sqlite:///./app.db", dest="dsn", help="sqlalchemy datbase uri")

(options, args) = parser.parse_args()
app.config['SECRET_KEY'] = md5(os.path.abspath(__file__))
app.config['JWT_LEEWAY'] = 3600 * 24 * 7
app.config['SESSION_TYPE'] = 'null'
app.config['SQLALCHEMY_DATABASE_URI'] = options.dsn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.getenv("FLASK_ENV","prod") == "dev":
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_ECHO'] = True
else:
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_ECHO'] = False

logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
logging.getLogger('google.auth.transport._mtls_helper').setLevel(logging.INFO)
logging.getLogger('google.auth.transport.requests').setLevel(logging.INFO)
logging.getLogger('google.cloud.ndb').setLevel(logging.INFO)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.info("options ====>>>: %s", options)
router.register(app)
JSONExceptionHandler(app)
Bootstrap(app)
cache.init_app(app)
JWT(app, authenticate, identity)
database.init(app)

CORS(app, resources={
    r"/api/*": {"origins": "*"}
})



if __name__ == '__main__':
    app.run(host=options.ip, port=options.port)
