from flask import jsonify,current_app
import traceback
import sys
import logging
from werkzeug.exceptions import HTTPException

from app.helpers.setting import Setting
from .helper import mail_send


class JSONExceptionHandler(object):

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def std_handler(self, error):
        if isinstance(error, HTTPException):
            msg = error.name
            code = error.code
            body = ""
        else:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = str(exc_value.args[0]) if len(exc_value.args) > 0 else "system error"
            code = exc_value.args[1] if len(exc_value.args) > 1 else 500

            if current_app and not current_app.debug:
                log = "msg: {},type:{},trace: {}".format(exc_value, exc_type, traceback.format_tb(exc_traceback))
                logging.error(log)
                body = []
                if len(exc_value.args) <= 1 or code == 505:
                    try:
                        mail_send(
                            Setting.get("ADMIN_EMAIL"),
                            "[Alarm]{}".format(str(error)),
                            "<b>{}</b>  {}<br />{}".format(exc_value, exc_type,
                                                           "<br />".join(traceback.format_tb(exc_traceback)))
                        )
                    except Exception as e:
                        logging.error("send email error: %s, %s", e, traceback.format_exc())
            else:
                body = [
                    str(exc_type),
                    traceback.format_tb(exc_traceback)
                ]

        response = jsonify(msg=msg, code=code, body=body)
        response.status_code = 200
        return response

    def init_app(self, app):
        self.register(HTTPException)

        @app.errorhandler(Exception)
        def internal_server_error(e):
            return self.std_handler(e)

        # for code, v in default_exceptions.iteritems():
        #     self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)
