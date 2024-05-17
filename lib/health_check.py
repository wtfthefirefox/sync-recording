from flask_restx import Resource
import logging
import requests
import traceback

from .api import api
from .config import config
from .exceptions import NotFoundError

cur_route = api.namespace("health_check", description="Check health of camera / room", path="/health_check/")

@cur_route.route("/<string:camera_id>")
class CameraHealthChecker(Resource):
    """
    Check if camera / room can record a video
    """
    def _get_cameras_url(self, camera_id):
        if camera_id in config._data["rooms"].cameraInfo:
            return [config._data["rooms"].cameraInfo[camera_id]["auto_host"]]
        elif camera_id in config._data["rooms"].camerasByRoom:
            result = []
            for camera in config._data["rooms"].camerasByRoom[camera_id]:
                result.append(camera["auto_host"])
            return result
        else:
            raise NotFoundError(f"camera or room with id {camera_id} not presented in config")

    def _check_camera_health(self, camera_id):
        try:
            request_url_base_path = f"{config._data['shinobi_url']}/{config._data['api_key']}/probe/{config._data['group_key']}?flag=default&url="
            for camera_url in self._get_cameras_url(camera_id):
                request_url = request_url_base_path + camera_url
                camera_health = requests.get(request_url, timeout=5)
                if not camera_health.json()["ok"]:
                    return False
            return True
        except NotFoundError:
            raise
        except Exception as e:
            logging.error(traceback.format_exc())
            return False

    def get(self, camera_id):
        return {"ok": self._check_camera_health(camera_id)}
