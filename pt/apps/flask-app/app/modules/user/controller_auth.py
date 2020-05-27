from flask import Blueprint, request, jsonify,current_app
import random
import logging
from datetime import datetime, timedelta
from .store_email_captcha import EmailCaptcha
from app.helpers.setting import Setting
from pt.libs.utils import check_email
from app.helpers.helper import mail_send
from pt.libs.flask_jwt import get_access_token
from app.helpers.auth import basic_auth
from app.libs.utils import generate_random, md5
from .store_user import User
from ..var.store import Var

app = Blueprint('user.auth', __name__)


@app.route('/api/auth/email/password/verify', methods=['post'])
def email_password_verify():
    """
    email password verify
    ---
    tags:
     - auth
    parameters:
      - name: email
        in: formData
        required: true
      - name: password
        in: formData
        required: true
    responses:
     200:
       description: ok
    """

    data = request.get_json()
    print(data)
    if data is None:
        email = request.form.get("email", None)
        password = request.form.get("password", None)
    else:
        email = data.get("email", None)
        password = data.get("password", None)

    if not check_email(email):
        raise Exception("不合法的Email", 500)

    user = User.get_by_email(email)
    if user is None:
        raise Exception("用户不存在", 500)

    if len(password) != 32:
        password = md5(password)

    if user.password != password:
        raise Exception("密码不正确", 500)

    access_token = get_access_token(user)

    return jsonify({"code": 200, "msg": "登录成功", "body": {
        "user": {
            "level": user.level,
            "expired_at": user.expired_at.timestamp() if user.expired_at is not None else 0
        },
        "access_token": "JWT " + access_token}})


@app.route('/api/auth/email/captcha/verify', methods=['post'])
def email_captcha_verify():
    """
    email captcha verify
    ---
    tags:
     - auth
    parameters:
      - name: email
        in: formData
        required: true
      - name: code
        in: formData
        required: true
    responses:
     200:
       description: ok
    """

    data = request.get_json()
    # print(data)
    if data is None:
        email = request.form.get("email", None)
        code = request.form.get("code", None)
    else:
        email = data.get("email", None)
        code = data.get("code", None)

    if not check_email(email):
        raise Exception("不合法的Email", 500)
    captcha = EmailCaptcha.get_by_email(email)
    if captcha is None:
        raise Exception("请重新发送验证码", 500)

    logging.debug(captcha)
    logging.debug("created_at: %s, expired_at: %s,now: %s", captcha.created_at,
                  captcha.created_at + timedelta(minutes=10), datetime.utcnow())

    if captcha is not None and captcha.code == code and captcha.created_at + timedelta(hours=1) > datetime.utcnow():
        user = User.get_by_email(email)
        msg = "登录成功"
        if user is None:
            msg = "登录成功,密码已发送到您的邮箱,请查收!"
            user = User(email=email, name=email.split("@")[0])

            if email in Setting.get("SUPER_EMAILS", default="SUPER_EMAILS1|SUPER_EMAIL2", update=True).split("|"):
                user.level = 0
            else:
                user.level = 1
            password = generate_random(6)
            template = Var.get("template-email-reg-ok.html", is_json=False)
            if template and "####################" in template:
                title = template.split("####################")[0].strip()
                content = template.split("####################")[1].strip()
                mail_send(
                    email,
                    title,
                    content.format(
                        email=email, password=password,
                        name=email.split("@")[0], balance_silver=user.balance_silver
                    )
                )
            user.password = md5(password)
            user.created_at = datetime.utcnow()
            user.updated_at = user.created_at
            User.put(user)

        access_token = get_access_token(user)
        EmailCaptcha.delete(captcha)

        return jsonify({"code": 200, "msg": msg, "body": {
            "user": {
                "level": user.level,
            },
            "access_token": "JWT " + access_token}})
    else:
        if captcha is not None and captcha.created_at + timedelta(hours=1) < datetime.utcnow():
            EmailCaptcha.delete(captcha)
            raise Exception("验证码已过期", 500)
        else:
            raise Exception("验证码不正确", 500)


@app.route('/api/auth/email/captcha', methods=['post'])
def email_captcha():
    """
    email captcha
    ---
    tags:
     - auth
    parameters:
      - name: email
        in: formData
        default: antonenkos933@gmail.com
        required: true
    responses:
     200:
       description: ok
    """
    data = request.get_json()
    if data is not None:
        email = data.get("email", None)
    else:
        email = request.form.get("email", None)
    if not check_email(email):
        raise Exception("不合法的Email", 500)

    captcha = EmailCaptcha.get_by_email(email)
    if captcha is not None and captcha.created_at + timedelta(minutes=1) > datetime.utcnow():
        raise Exception("验证码已经发送,请一分钟之后再试", 500)
    else:
        if current_app.debug:
            code = 9999
        else:
            code = str(random.randrange(1000, 9999))
        if captcha is not None:
            captcha.code = code
            captcha.created_at = datetime.utcnow()
            captcha.updated_at = datetime.utcnow()
        else:
            captcha = EmailCaptcha(
                code=code, email=email,
                created_at=datetime.utcnow(), updated_at=datetime.utcnow()
            )
        logging.info(captcha)
        EmailCaptcha.put(captcha)
        template = Var.get("template-email-captcha.html", is_json=False)
        if template and "####################" in template:
            title = template.split("")[0].strip()
            content = template.split("####################")[1].strip()
            mail_send(
                email,
                title.format(captcha_code=code),
                content.format(name=email.split("@")[0])
            )
        return jsonify({"code": 200, "msg": "验证码发送成功,请查收"})


@app.route('/api/auth/email/set/level', methods=['post'])
@basic_auth.login_required
def email_auth_set_level():
    """
    email_auth_set_level
    ---
    tags:
     - auth
    parameters:
      - name: email
        in: formData
        required: true
      - name: level
        in: formData
        required: true
        default: 0
    responses:
     200:
       description: ok
    """
    data = request.get_json()
    print(data)
    if data is None:
        email = request.form.get("email", None)
        level = request.form.get("level", None)
    else:
        email = data.get("email", None)
        level = data.get("level", None)

    if not check_email(email):
        raise Exception("不合法的Email", 500)

    user = User.get_by_email(email)
    if user is None:
        raise Exception("用户不存在", 500)
    user.level = int(level)
    user = User.put(user)
    return jsonify({"code": 200, "msg": "", "body": User.to_dict(user)})
