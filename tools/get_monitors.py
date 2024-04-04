import json


def get_monitors_by_room(input_file, room_name):
    with open(input_file, "r") as file:
        config = json.load(file)
    cams = []
    for room in config:
        if room["room_name"] == room_name:
            for camera in room["cameras"]:
                cams.append(camera["mid"])
    return cams
