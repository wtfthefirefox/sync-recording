import os

from flask import send_file, request
from flask_restx import Resource
from .exceptions import NotFoundError

from .api import api

from .config import config

TEST_CONFIG_PATH = "test_files"
cur_route = api.namespace("downloading", description="download API", path="/download/")

@cur_route.route("/file/<string:file_name>/")
class DownladFile(Resource):
    """
    Download file with name in selected folder
    """

    def get(self, file_name):
        folder_path = request.args.get("folder_path")
        file_path = os.path.join(folder_path if folder_path else "", file_name)
        file_name_base_path = ""
        # TODO: Add check for .. in folder_path
        if config["is_test"]:
           file_name_base_path = os.path.join(os.path.join(os.getcwd(), TEST_CONFIG_PATH), file_path) 
        else:
            file_name_base_path = os.path.join(config["export_dir"], file_path)
        if not os.path.exists(file_name_base_path) or not os.path.isfile(file_name_base_path):
            if folder_path:
                raise NotFoundError(f"File with name {file_name} in folder {folder_path} does not exists")
            else:
                raise NotFoundError(f"File with name {file_name} does not exists")
    
        return send_file(file_name_base_path, as_attachment=True)
