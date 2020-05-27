from . import common
from . import var
from . import user


def register(app):
    app.register_blueprint(common.common.app)
    app.register_blueprint(common.constant.app)
    app.register_blueprint(common.swagger.app)
    app.register_blueprint(common.var.app)
    app.register_blueprint(var.controller_admin.app)
    app.register_blueprint(user.controller_auth.app)
    app.register_blueprint(user.controller_user.app)
    app.register_blueprint(user.controller_admin.app)

