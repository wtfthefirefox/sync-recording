from flask import Blueprint
from flask_restx import Api


blueprint = Blueprint("api", "sync-recording", url_prefix="/api/v1")
api = Api(blueprint, version="1.0", ui=False)
