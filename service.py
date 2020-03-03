from flask import Flask, request, abort
import requests
import uuid

from sesamutils.flask import serve
from sesamutils import sesam_logger, VariablesConfig


app = Flask(__name__)
logger = sesam_logger("Slack command receiver",)

req_vars = ["NODE_JWT", "VALIDATION_TOKEN", "ENDPOINT_URL"]
config = VariablesConfig(req_vars)

if not config.validate():
    logger.error("Missing required variable(s).")

headers = {
    "Authorization": f"bearer {config.NODE_JWT}"
}


def valid_token(token):
    return token == config.VALIDATION_TOKEN


@app.route("/command", methods=["POST"])
def command():
    _id = str(uuid.uuid1())
    data = dict(request.form)
    data["_id"] = _id
    token = data.pop("token")
    if not valid_token(token):
        logger.info("Invalid token. Aborting")
        return abort(403)
    logger.info("Valid command received. Pushing to pipe endpoint")
    resp = requests.post(config.ENDPOINT_URL, json=data, headers=headers)
    logger.debug(resp.status_code)
    logger.debug(resp.text)
    resp.raise_for_status()
    return "", 200


# Start the server on port 3000
if __name__ == "__main__":
    serve(app)
