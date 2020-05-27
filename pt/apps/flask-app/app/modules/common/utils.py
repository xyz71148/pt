from flask import jsonify, Blueprint,request
from pt.libs.cloudflare import CloudFlare

from app.helpers.helper import mail_send
from app.helpers.auth import basic_auth
from app.helpers.setting import Setting

app = Blueprint('utils', __name__)


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
    mail_send(email, title, content)
    body = ""
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
    obj = CloudFlare(Setting.get("CloudflareAuthEmail"), Setting.get("CloudflareAuthKey"))
    obj.get_zone_id(domain)
    body = obj.update_domain_ip(ip, domain)
    return jsonify(body)
