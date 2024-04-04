import argparse
import json


def get_monitors_by_room(input_json, output_file, room_name):
    with open(args.input_json, 'r') as file:
        config = json.load(file)

    with open(args.output_file, 'w') as file:
        cams = []
        for room in config:
            if room['room_name'] == room_name:
                for camera in room['cameras']:
                    cams.append(camera['mid'])

        json.dump(cams, file)

    print(cams)


parser = argparse.ArgumentParser(description="Добавление камеры в Shinobi")
parser.add_argument("--input_json", help="Путь до json'a с камерами")
parser.add_argument("--output_file", help="Путь до выходного файла с камерами из указанной комнаты")
parser.add_argument("--room", help="Номер нужной комнаты")

args = parser.parse_args()
get_monitors_by_room(args.input_json, args.output_file, args.room)