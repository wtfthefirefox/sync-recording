import requests
import datetime
import asyncio
import json
import argparse


class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id


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


def record_request(ip, api, group_key, cameras):
    for camera in cameras:
        trigger_url = ip + '/' + api + '/monitor/' + group_key + '/' + camera + '/record/' + time
        try:
            print("Send record request to ", camera)
            response = requests.get(trigger_url)
            if response.status_code == 200:
                now = datetime.datetime.now()
                print(now.time())
                print('Recording started for ', camera)
                print(response.json())
            else:
                print('GET request failed. Error:', response.status_code)
        except Exception as e:
            print(f'Error starting recording: {e}')


async def record(ip, api, group_key, room):
    cameras_id = room.cameras_id
    room_id = room.room_id
    print("Start recording")
    new_cameras_id = []
    for camera in cameras_id:
        new_cameras_id.append(camera + "_")
    try:
        with open('room_states.json', 'r') as file:
            for line in file:
                room_states = json.loads(line)
                if room_id in room_states and room_states[room_id] == "recording":
                    print("Recording is already in progress for this room.")
                    return
            file.close()
    except FileNotFoundError:
        pass
    while True:
        record_request(ip, api, group_key, cameras_id)
        save_room_state(room_id, "recording")

        await asyncio.sleep(diff_secs)

        with open('room_states.json', 'r') as file:
            for line in file:
                room_states = json.loads(line)
                if room_id in room_states and room_states[room_id] == "stop":
                    print("Recording stopped for this room.")
                    return
            file.close()

        record_request(ip, api, group_key, new_cameras_id)
        save_room_state(room_id, "recording")

        await asyncio.sleep(diff_secs)


async def main():
    parser = argparse.ArgumentParser(description="Начало записи")
    parser.add_argument("--ip", help="IP-адрес для доступа к Shinobi", default="http://84.201.177.141:8080")
    parser.add_argument("--api", help="API для доступа к Shinobi", default="fYNVjZNfYuqmdt9DecSHeigZ7yPmX5")
    parser.add_argument("--group_key", help="Ваш ключ группы", default="iIK9Z11DJ1")
    parser.add_argument("--room", help="Комната в Json", default='{"abc": ["304_3"]}')

    args = parser.parse_args()
    room_json = json.loads(args.room)
    room_id = list(room_json.keys())[0]
    cameras_id = room_json[room_id]

    room = Room(room_id, cameras_id)

    await record(args.ip, args.api, args.group_key, room)


if __name__ == '__main__':
    asyncio.run(main())
