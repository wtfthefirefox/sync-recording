import requests
import datetime
import asyncio
import os
import cv2

import argparse


class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id


def trigger(ip, api, group_key, cameras):
    for camera in cameras:
        trigger_url = ip + '/' + api + '/motion/' + group_key + '/%camera%?data={"plug":"Force trigger","name":"Home-Assistant","reason":"TRY_TO_RECORD","confidence":100}'
        try:
            print("Send trigger request to ", camera)
            response1 = requests.get(trigger_url.replace("%camera%", camera))
            if response1.status_code == 200:
                now1 = datetime.datetime.now()
                print(now1.time())
                print('Recording started with trigger for ', camera)
                print(response1.json())
            else:
                print('GET request failed. Error:', response1.status_code)
        except Exception as e:
            print(f'Error stopping recording: {e}')

async def record(ip, api, group_key, minutes_to_record, room):
    """
        Record specified minutes from selected room

        If the argument `minutes_to_record` = -1 then video
        will be record while STOP command not entered.

        Parameters
        ----------
        minutes_to_record : int

        room_id : str
    """
    cameras_id = room.cameras_id
    print("Start recording")

    while minutes_to_record > 0:
        trigger(ip, api, group_key, cameras_id)
        await asyncio.sleep(64)
        minutes_to_record -= 1

    if minutes_to_record == -1:
        stop_recording = False
        while not stop_recording:
            for camera in cameras_id:
                trigger(ip, api, group_key, camera)
            await asyncio.sleep(64)
            user_input = input("Enter 'STOP' to stop recording: ")
            if user_input == "STOP":
                stop_recording = True


async def main():
    parser = argparse.ArgumentParser(description="Начало записи")
    parser.add_argument("--ip", help="IP-адрес для доступа к Shinobi", default="http://0.0.0.0:8080")
    parser.add_argument("--api", help="API для доступа к Shinobi", default="0")
    parser.add_argument("--group_key", help="Ваш ключ группы", default="1")
    parser.add_argument("--time", help="Длительность записи в минутах", default=4)
    parser.add_argument("--room", help="Комната в Json", default=Room("abc", ["305_3"]))

    parser.add_argument("--folder", help="Главная папка, в которой хранятся папки с записями",
                        default="/home/Shinobi/videos")
    parser.add_argument("--audio_file",
                        help="Путь к видео, аудиозапись которого необходимо наложить на остальные записи.",
                        default="/home/Shinobi/videos/test/main.mp4")

    args = parser.parse_args()
    await record(args.ip, args.api, args.group_key, args.time, args.room)


if __name__ == '__main__':
    asyncio.run(main())
