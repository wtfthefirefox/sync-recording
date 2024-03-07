
from flask import Flask
from marshmallow.exceptions import ValidationError

from .api import api, blueprint
from .cache import cache
from .config import config
from .exceptions import (
    AuthenticationError,
    BadGatewayError,
    ForbiddenError,
    RequestParamsError,
)

from .download import *  # noqa


def create_app(name, config_path):
    app = Flask(name)
    app.register_blueprint(blueprint)
    app.config["PROPAGATE_EXCEPTIONS"] = False
    cache.init_app(app)

    config.load_from(config_path)

    @api.errorhandler(RequestParamsError)
    def handle_request_params_error(error):
        return {"message": str(error)}, 400

    @api.errorhandler(ValidationError)
    def handle_marshmallow_validation_error(error):
        del error.data
        return {"error": str(error.messages)}, 400

    @api.errorhandler(ForbiddenError)
    def handle_permissions_error(error):
        return {"message": str(error)}, 403

    @api.errorhandler(BadGatewayError)
    def handle_bad_gateway_error(error):
        return {"message": str(error)}, 502

    return app
