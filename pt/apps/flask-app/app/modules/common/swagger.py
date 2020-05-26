from flask import jsonify, Blueprint, render_template
from app.libs import utils
from app.helpers.setting import Setting

app = Blueprint('swagger', __name__)


def get_spec(swag):
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "iAPI"

    swag['contact'] = dict()
    swag['contact']['Support'] = ""

    swag['securityDefinitions'] = dict(
        apiKeyAuth=dict(
            type="apiKey",
            name="Authorization",
        )
    )

    swag['definitions'] = dict(
        JsonRequest=dict(
            type="object",
            properties=dict(
                data=dict(
                    type="string",
                )
            ),
        ),
        SettingRequest=dict(
            type="object",
            properties=dict(
                value=dict(
                    type="string",
                )
            ),
        ),
        ServicesRequest=dict(
            type="object",
            properties=dict(
                services=dict(
                    type="object",
                )
            ),
        ),
        ApiResponse=dict(
            type="object",
            properties=dict(
                code=dict(
                    type="integer",
                    format="int32"
                ),
                body=dict(
                    type="object",
                ),
                msg=dict(
                    type="string",
                )
            ),
        )
    )
    swag['securityDefinitions']['apiKeyAuth']['in'] = 'header'
    return swag


@app.route("/api/ping", methods=['GET'])
def ping():
    """
    Ping
    ---
    tags:
      - utils
    responses:
      200:
        description: ok
    """
    return jsonify({"code": 200, "body": "dong"})


@app.route("/swagger")
def swagger():
    if Setting.get("DISABLE_SWAGGER", default="false", update=True) == "true":
        raise Exception("DISABLED", 403)
    swagger_api_url = utils.get_base_url() + "/api/spec"
    return render_template('swagger.html', swagger_api_url=swagger_api_url)

