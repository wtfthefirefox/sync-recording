import os

from flask import send_file
from flask_restx import Resource

from .api import api
from .models import DownloadFile


cur_route = api.namespace("downloading", description="Profile API", path="/download/")

@cur_route.route("/file/<string:file_name>/")
class ProfileView(Resource):
    """
    Download file with name
    """

    def get(self, file_name):
        file_name_base_path = os.path.join("some_local", file_name)

        if not os.path.exists(file_name_base_path):
            raise RuntimeError(f"File with name {file_name} does not exists")

        return send_file(file_name_base_path, as_attachment=True)
