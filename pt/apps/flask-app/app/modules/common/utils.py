from flask import Blueprint, jsonify,request
from lib import iemail
from lib.base_auth import basic_auth
from control.content.store import Content
from models.setting import Setting
from models.instance import Instance
import os
import simplejson as json
from lib.cloudflare import update_ip_domain
from control.compute import mail
app = Blueprint('utils', __name__)







@app.route('/api/utils/turnserver/auth', methods=['GET'])
def utils_turnserver_auth():
    """
    utils
    ---
    tags:
     - utils
    parameters: []
    responses:
     200:
       description: ok
    """

    secret = Setting.get("TurnServerSecret", default="secret", update=True)
    expiry = Setting.get("TurnServerExpiry", default="8400", update=True)
    host = Setting.get("TurnServerHost", default="ws.japp.cc:3478", update=True)
    wss_instance_host = Setting.get("WSS_INSTANCE_HOST", default="ws.japp.cc:443", update=True)

    cmd = """
secret={secret} && \
time=$(date +%s) && \
expiry={expiry} && \
username=$(( $time + $expiry )) &&\
echo $username && \
echo $(echo -n $username | openssl dgst -binary -sha1 -hmac $secret | openssl base64)"""\
        .format(secret=secret, expiry=expiry)

    credential = os.popen(cmd).read().split("\n")

    body = {
        "wss_instance_host": wss_instance_host,
        "ice_server": [
            {
                "urls": [
                    "turn:"+host+"?transport=udp",
                    "turn:"+host+"?transport=tcp"
                ],
                "username": credential[0],
                "credential": credential[1]
            },
            {
                "urls": [
                    "stun:"+host
                ]
            }
        ]
    }
    return jsonify(body=body)


@app.route('/api/utils', methods=['GET'])
def utils():
    """
    utils
    ---
    security:
     - apiKeyAuth : []
    tags:
     - utils
    parameters: []
    responses:
     200:
       description: ok
    """
    body = ""
    return jsonify(body=body)


@app.route('/api/utils/email', methods=['POST'])
@basic_auth.login_required
def utils_email():
    """
    utils_email
    ---
    tags:
     - utils
    parameters:
      - name: email
        in: formData
        required: true
      - name: title
        in: formData
        required: true
      - name: content
        in: formData
        required: true
    responses:
     200:
       description: ok
    """
    email = request.form.get("email", None)
    title = request.form.get("title", None)
    content = request.form.get("content", None)
    iemail.send(email, title, content)
    body = ""
    return jsonify(body=body)


@app.route('/api/utils/email/test', methods=['POST'])
@basic_auth.login_required
def utils_email_test():
    """
    utils_email
    ---
    tags:
     - utils
    parameters:
      - name: email
        in: formData
        default: dhole.me@gmail.com
        required: true
      - name: name
        in: formData
        required: true
    responses:
     200:
       description: ok
    """
    email = request.form.get("email", None)
    name = request.form.get("name", None)
    instance = Instance.row_by_name(name)
    res1 = mail.create_instance_ok(email,instance=Instance.get_detail(instance))
    res2 = mail.instance_del_ok(email,instance=Instance.get_detail(instance))
    res3 = mail.instance_ip_ok(email,instance=Instance.get_detail(instance))
    res4 = mail.instance_port_ok(email,instance=Instance.get_detail(instance))
    body = [
        res1,res2,res3,res4
    ]
    return jsonify(body=body)


@app.route('/api/utils/domain', methods=['POST'])
@basic_auth.login_required
def utils_domain():
    """
    utils_domain
    ---
    tags:
     - utils
    parameters:
      - name: ip
        in: formData
        required: true
      - name: domain
        in: formData
        required: true
    responses:
     200:
       description: ok
    """

    ip = request.form.get("ip", None)
    domain = request.form.get("domain", None)
    if ip is None or domain is None:
        raise Exception("ip or domain is invalid")
    if Setting.get("CloudflareZone") not in domain:
        raise Exception("domain is not allow")
    body = update_ip_domain(ip, domain)
    return jsonify(body=body)
