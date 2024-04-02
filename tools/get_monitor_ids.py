import json

with open('sample.json', 'r') as data:
    sample = json.load(data)


def get_monitor_ids(config: list, room_name: str) -> list:
    cameras = []
    for room in config:
        if room['room_name'] == room_name:
            for camera in room['cameras']:
                cameras.append(camera['mid'])

    return cameras


print(get_monitor_ids(sample, '305'))
