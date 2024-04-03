import argparse
import json


def get_monitor_ids(config: list, room_name: str) -> list:
    cams = []
    for room in config:
        if room['room_name'] == room_name:
            for camera in room['cameras']:
                cams.append(camera['mid'])

    return cams


parser = argparse.ArgumentParser(description="Добавление камеры в Shinobi")
parser.add_argument("--input_json", help="Путь до json'a с камерами")
parser.add_argument("--output_file", help="Путь до выходного файла с камерами из указанной комнаты")
parser.add_argument("--room", help="Номер нужной комнаты")

args = parser.parse_args()
with open(args.input_json, 'r') as file:
    data = json.load(file)

with open(args.output_file, 'w') as file:
    cameras = get_monitor_ids(data, args.room)
    json.dump(cameras, file)

print(cameras)
