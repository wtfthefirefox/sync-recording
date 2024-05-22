from flask_restx import Resource
from flask import request
import asyncio
import datetime
import json
import os
import requests
import subprocess

from .config import config
from .api import api
from .exceptions import NotFoundError

RECORDING_TIME = "1/min"
RECORDS_DIFF = 33 # time dif between records

cur_route = api.namespace("record", description="Recording API", path="/record/")

class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id


def record_request(cameras):
    ip = config._data["shinobi_url"]
    api_path = config._data["api_key"]
    group_key = config._data["group_key"]

    for camera in cameras:
        trigger_url = f"{ip}/{api_path}/monitor/{group_key}/{camera}/record/{RECORDING_TIME}"
        try:
            print("Send record request to ", camera)
            response = requests.get(trigger_url)
            if response.status_code == 200:
                now = datetime.datetime.now()
                print(now.time(), "Recording started for ", camera, response.json())
            else:
                print("GET request failed with error:", response.status_code)
        except Exception as e:
            print(f"Error starting recording: {e}")


def save_room_state(room_id, state):
    try:
        with open("../room_states.json", "r") as file:
            room_states = json.load(file)
    except FileNotFoundError:
        room_states = {}

    room_states[room_id] = state

    try:
        with open("../room_states.json", "w") as file:
            json.dump(room_states, file)
            file.close()
    except OSError as e:
        print("Error while creating database file! Check permissions for this folder.", e)


async def record(room):
    cameras_id = room.cameras_id
    room_id = room.room_id
    print("Recoding started")
    new_cameras_id = []
    for camera in cameras_id:
        new_cameras_id.append(camera + "_")
    try:
        with open("../room_states.json", "r") as file:
            for line in file:
                room_states = json.loads(line)
                if room_id in room_states and room_states[room_id] == "recording":
                    print("Recording is already in progress for this room.")
                    return
            file.close()
    except FileNotFoundError:
        pass
    while True:
        record_request(cameras_id)
        save_room_state(room_id, "recording")

        await asyncio.sleep(RECORDS_DIFF)

        with open("../room_states.json", "r") as file:
            for line in file:
                room_states = json.loads(line)
                if room_id in room_states and room_states[room_id] == "stop":
                    print("Recording stopped for this room.")
                    return
            file.close()

        record_request(new_cameras_id)
        save_room_state(room_id, "recording")

        await asyncio.sleep(RECORDS_DIFF)


@cur_route.route("/start")
class RecordStart(Resource):
    def post(self):
        request_data = request.get_data().decode('utf-8')
        room_id = request_data["room_id"]
        cameras = []
        if room_id in config._data["rooms"].camerasByRoom:
            for camera in config._data["rooms"].camerasByRoom[room_id]:
                cameras.append(camera["mid"])
        else:
            raise NotFoundError(f"room with id {room_id} not presented in config")

        print(cameras)
        room = Room(room_id, cameras)
        asyncio.run(record(room))
        return {"message": "Recording started"}, 200


class Video:
    def __init__(self, filename, start_time, end_time):
        self.filename = filename
        self.start_time = start_time
        self.end_time = end_time


def save_room_state(room_id, state):
    try:
        with open("room_states.json", "r") as file:
            room_states = json.load(file)
    except FileNotFoundError:
        room_states = {}

    room_states[room_id] = state

    try:
        with open("room_states.json", "w") as file:
            json.dump(room_states, file)
            file.close()
            print("State saved")
    except OSError as e:
        print(e)
        print("Error while creating database file! Check permissions for this folder.")


def stop_request(ip, api, group_key, cameras):
    new_cameras = []
    for c in cameras:
        new_cameras.append(c)
        new_cameras.append(c + "_")
    for camera in new_cameras:
        trigger_url = ip + "/" + api + "/monitor/" + group_key + "/" + camera + "/start"
        try:
            print("Send stop request to ", camera)
            response = requests.get(trigger_url)
            if response.status_code == 200:
                now = datetime.datetime.now()
                print(now.time())
                print("Recording stopped for ", camera)
                print(response.json())
            else:
                print("GET request failed. Error:", response.status_code)
        except Exception as e:
            print(f"Error stopping recording: {e}")


def get_videos(ip, api, group_key, cameras):
    new_cameras = []
    for c in cameras:
        new_cameras.append(c)
        new_cameras.append(c + "_")
    camera_video = {}
    for camera in new_cameras:
        trigger_url = ip + "/" + api + "/videos/" + group_key + "/" + camera
        try:
            response = requests.get(trigger_url)
            if response.status_code == 200:
                now = datetime.datetime.now()
                print(now.time())
                response_json = json.loads(response.text)
                videos_info = response_json["videos"]

                videos_list = []

                for video_info in videos_info:
                    filename = video_info["filename"]
                    start_time = video_info["time"]
                    end_time = video_info["end"]
                    videos_list.append(Video(filename, start_time, end_time))
                camera_video[camera] = videos_list
            else:
                print("GET request failed. Error:", response.status_code)
        except Exception as e:
            print(f"Error stopping recording: {e}")
    return camera_video


def merge_videos(room, videos_list, folder):
    # Предполагается, что "folder" - это путь к директории, где будут сохраняться временные и итоговые файлы.
    for camera in room.cameras_id:
        videos1 = sorted(videos_list[camera], key=lambda x: datetime.datetime.strptime(x.start_time, "%Y-%m-%dT%H:%M:%SZ"))
        videos2 = sorted(videos_list[camera + "_"], key=lambda x: datetime.datetime.strptime(x.start_time, "%Y-%m-%dT%H:%M:%SZ"))
        # Создаем файл списка для ffmpeg
        list_filename = f"{folder}/merge_list.txt"
        with open(list_filename, "w") as list_file:
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
        date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
        merge_command = [
            "/opt/homebrew/bin/ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_filename,
            "-c", "copy",
            f"{folder}/{room.room_id}_merged_{date_str}.mp4"
        ]
        # Выполнение команды склейки
        subprocess.run(merge_command)
        # Удаление временного файла списка
        os.remove(list_filename)


async def stop(room, folder):
    ip = config._data["shinobi_url"]
    api_path = config._data["api_key"]
    group_key = config._data["group_key"]
    room_id = room.room_id
    print("Stop recording")
    save_room_state(room_id, "stop")
    stop_request(ip, api_path, group_key, room.cameras_id)
    videos_list = get_videos(ip, api_path, group_key, room.cameras_id)
    merge_videos(room, videos_list, folder)


@cur_route.route("/stop")
class RecordStop(Resource):
    def post(self):
        request_data = request.get_data().decode('utf-8')
        room_id = request_data["room_id"]
        cameras = []
        if room_id in config._data["rooms"].camerasByRoom:
            for camera in config._data["rooms"].camerasByRoom[room_id]:
                cameras.append(camera["mid"])
        else:
            raise NotFoundError(f"room with id {room_id} not presented in config")
        room = Room(room_id, cameras)

        asyncio.run(stop(room, config._data["export_dir"]))
        return {"message": "Recording started"}, 200
