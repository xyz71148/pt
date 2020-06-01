from . import common
from . import var
from . import user
from . import task


def register(app):
    app.register_blueprint(common.common.app)
    app.register_blueprint(common.constant.app)
    app.register_blueprint(common.swagger.app)
    app.register_blueprint(common.utils.app)
    app.register_blueprint(common.var.app)

    app.register_blueprint(var.controller_admin.app)
    app.register_blueprint(task.controller_admin.app)
    app.register_blueprint(user.controller_auth.app)
    app.register_blueprint(user.controller_user.app)
    app.register_blueprint(user.controller_admin.app)

