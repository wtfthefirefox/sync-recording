from flask_restx import Resource, Namespace, fields
from flask import request
import requests
import datetime
import asyncio
import json

from test.config import config
from .api import api

cur_route = api.namespace('record_stop', description='Start recording of camera / room')

class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id

class Video:
    def __init__(self, filename, start_time, end_time):
        self.filename = filename
        self.start_time = start_time
        self.end_time = end_time

time = "1/min"
diff_secs = 33

def save_room_state(room_id, state):
    try:
        with open('room_states.json', 'r') as file:
            room_states = json.load(file)
    except FileNotFoundError:
        room_states = {}

    room_states[room_id] = state

    try:
        with open('room_states.json', 'w') as file:
            json.dump(room_states, file)
            file.close()
    except OSError as e:
        print(e)
        print("Error while creating database file! Check permissions for this folder.")


def stop_request(ip, api, group_key, cameras):
    new_cameras = []
    for c in cameras:
        new_cameras.append(c)
        new_cameras.append(c + "_")
    for camera in new_cameras:
        trigger_url = ip + '/' + api + '/monitor/' + group_key + '/' + camera + '/start'
        try:
            print("Send stop request to ", camera)
            response = requests.get(trigger_url)
            if response.status_code == 200:
                now = datetime.datetime.now()
                print(now.time())
                print('Recording stopped for ', camera)
                print(response.json())
            else:
                print('GET request failed. Error:', response.status_code)
        except Exception as e:
            print(f'Error stopping recording: {e}')


def get_videos(ip, api, group_key, cameras):
    new_cameras = []
    for c in cameras:
        new_cameras.append(c)
        new_cameras.append(c + "_")
    camera_video = {}
    for camera in new_cameras:
        trigger_url = ip + '/' + api + '/videos/' + group_key + '/' + camera
        try:
            response = requests.get(trigger_url)
            if response.status_code == 200:
                now = datetime.datetime.now()
                print(now.time())
                response_json = json.loads(response.text)
                videos_info = response_json['videos']

                videos_list = []

                for video_info in videos_info:
                    filename = video_info['filename']
                    start_time = video_info['time']
                    end_time = video_info['end']
                    videos_list.append(Video(filename, start_time, end_time))
                camera_video[camera] = videos_list
            else:
                print('GET request failed. Error:', response.status_code)
        except Exception as e:
            print(f'Error stopping recording: {e}')
    return camera_video

import subprocess

def merge_videos(room, videos_list, folder):
    # Предполагается, что 'folder' - это путь к директории, где будут сохраняться временные и итоговые файлы.
    for camera in room.cameras_id:
        videos1 = sorted(videos_list[camera], key=lambda x: datetime.datetime.strptime(x.start_time, '%Y-%m-%dT%H:%M:%SZ'))
        videos2 = sorted(videos_list[camera + "_"], key=lambda x: datetime.datetime.strptime(x.start_time, '%Y-%m-%dT%H:%M:%SZ'))
        # Создаем файл списка для ffmpeg
        list_filename = f"{folder}/merge_list.txt"
        with open(list_filename, 'w') as list_file:
            # Добавляем первые 45 секунд из первого видео
            list_file.write(f"file '{camera}/{videos1[0].filename}'\n")
            list_file.write(f"inpoint 0\n")
            list_file.write(f"outpoint 45\n")
            # Для всех последующих видео берем 30 секундные сегменты, начиная с 15-й секунды
            for v1, v2 in zip(videos1[1:], videos2):
                list_file.write(f"file '{camera}_/{v2.filename}'\n")
                list_file.write(f"inpoint 15\n")  # Начало с 15-й секунды
                list_file.write(f"outpoint 45\n")  # Конец на 45-й секунде
                list_file.write(f"file '{camera}/{v1.filename}'\n")
                list_file.write(f"inpoint 15\n")  # То же для второго списка видео
                if v1 != videos1[-1]:
                    list_file.write(f"outpoint 45\n")
        # Команда для склейки видео с использованием ffmpeg
        merge_command = [
            '/opt/homebrew/bin/ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_filename,
            '-c', 'copy',
            f"{folder}/merged.mp4"
        ]
        # Выполнение команды склейки
        subprocess.run(merge_command)
        # Удаление временного файла списка
        #os.remove(list_filename)


async def stop(room, folder):
    ip = config._data["ip"]
    api_path = config._data["api"]
    group_key = config._data["group_key"]
    room_id = room.room_id
    print("Stop recording")
    save_room_state(room_id, "stop")
    stop_request(ip, api_path, group_key, room.cameras_id)
    videos_list = get_videos(ip, api_path, group_key, room.cameras_id)
    merge_videos(room, videos_list, folder)


@cur_route.route('/')
class RecordStarter(Resource):

    def post(self):
        data = request.json
        room_json = json.loads(data["room"])
        room_id = list(room_json.keys())[0]
        cameras_id = room_json[room_id]
        room = Room(room_id, cameras_id)
        asyncio.run(stop(room, data["folder"]))
        return {'message': 'Recording started'}, 200

