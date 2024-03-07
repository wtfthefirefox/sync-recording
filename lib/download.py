import os

from flask import send_file
from flask_restx import Resource
from marshmallow.exceptions import ValidationError

from .api import api
from .models import DownloadFile

from .config import config

TEST_CONFIG_PATH = "test_files"
cur_route = api.namespace("downloading", description="Profile API", path="/download/")

@cur_route.route("/file/<string:file_name>/")
class ProfileView(Resource):
    """
    Download file with name
    """

    def get(self, file_name):
        file_name_base_path = ""
        if config["is_test"]:
           file_name_base_path = os.path.join(os.path.join(os.getcwd(), TEST_CONFIG_PATH), file_name) 
        else:
            file_name_base_path = os.path.join(config["export_dir"], file_name)

        if not os.path.exists(file_name_base_path):
            raise ValidationError(f"File with name {file_name} does not exists")

        return send_file(file_name_base_path, as_attachment=True)
