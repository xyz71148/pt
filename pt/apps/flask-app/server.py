import os
import hashlib
import logging
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_swagger import swagger
from pt.libs.utils import set_logging
from pt.libs.flask_jwt import JWT

from app.helpers.helper import cache
from app.helpers.auth import basic_auth
from app.helpers.pt_exception import JSONExceptionHandler
from app.modules.user.store_user import User

from app.modules.var.store import db as var_db
from app.modules.user.store_user import db as store_user_db
from app.modules.user.store_email_captcha import db as store_email_captcha_db

from app.helpers.setting import Setting
from app.modules import router
from flask_sqlalchemy import SQLAlchemy

from app.modules.common.swagger import get_spec

os.system("export")
app = Flask(__name__)
app.config['SECRET_KEY'] = hashlib.md5(os.path.abspath(__file__).encode('utf-8')).hexdigest()
app.config['JWT_LEEWAY'] = 3600 * 24 * 7
app.config['SESSION_TYPE'] = 'null'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/test'
# 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 查询时显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

logFormatter = '[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s %m-%d %H:%M:%S'

flask_env = os.getenv("AP_FLASK_ENV", "prod")

if flask_env == "dev":
    app.config['DEBUG'] = True
    set_logging(logging.DEBUG)
else:
    app.config['DEBUG'] = False
    set_logging(logging.INFO)


logging.info("FLASK_ENV is %s", flask_env)
db = SQLAlchemy(app)

router.register(app)
JSONExceptionHandler(app)
Bootstrap(app)
cache.init_app(app)

CORS(app, resources={
    r"/api/*": {"origins": "*"}
})



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


JWT(app, authenticate, identity)

if __name__ == '__main__':
    var_db.init_app(app)
    with app.app_context():
        var_db.create_all()
        store_user_db.create_all()
        store_email_captcha_db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8083)
