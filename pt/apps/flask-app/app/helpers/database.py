
from app.modules.var.store import db as var_db
from app.modules.task.store import db as task_db
from app.modules.user.store_user import db as store_user_db
from app.modules.user.store_email_captcha import db as store_email_captcha_db


def init(app):
    var_db.init_app(app)
    store_user_db.init_app(app)
    task_db.init_app(app)
    store_email_captcha_db.init_app(app)

    with app.app_context():

        # var_db.drop_all()
        # store_user_db.drop_all()
        # store_email_captcha_db.drop_all()

        var_db.create_all()
        task_db.create_all()
        store_user_db.create_all()
        store_email_captcha_db.create_all()