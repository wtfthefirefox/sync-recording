from collections import namedtuple
import json


def get_monitors_info(input_file):
    RoomsInfo = namedtuple("RoomsInfo", ["camerasByRoom", "cameraToRoom", "cameraInfo"])
    with open(input_file, "r") as file:
        config = json.load(file)
    cameras_by_room = {}
    camera_to_room = {}
    camera_info = {}
    for room in config:
        cameras_by_room[room["room_name"]] = room["cameras"]
        for camera in room["cameras"]:
            camera_to_room[camera["mid"]] = room
            camera_info[camera["mid"]] = camera
    return RoomsInfo(cameras_by_room, camera_to_room, camera_info)
