from flask_restx import Resource, Namespace, fields
from flask import request
import requests
import datetime
import asyncio
import json

from test.config import config

api = Namespace('record', description='Start recording of camera / room')

record_model = api.model('Record', {
    'room_id': fields.String(required=True, description='Room ID'),
    'cameras_id': fields.List(fields.String, description='List of Camera IDs')
})


class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id


def record_request(cameras):
    ip = config._data["ip"]
    api_path = config._data["api"]
    group_key = config._data["group_key"]
    time = "1/min"  # Это значение можно вынести в конфигурацию, если оно изменяется
    for camera in cameras:
        trigger_url = f"{ip}/{api_path}/monitor/{group_key}/{camera}/record/{time}"
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


time = "1/min"
diff_secs = 33

def save_room_state(room_id, state):
    try:
        with open('../room_states.json', 'r') as file:
            room_states = json.load(file)
    except FileNotFoundError:
        room_states = {}

    room_states[room_id] = state

    try:
        with open('../room_states.json', 'w') as file:
            json.dump(room_states, file)
            file.close()
    except OSError as e:
        print(e)
        print("Error while creating database file! Check permissions for this folder.")


async def record(room):
    cameras_id = room.cameras_id
    room_id = room.room_id
    print("Start recording")
    new_cameras_id = []
    for camera in cameras_id:
        new_cameras_id.append(camera + "_")
    try:
        with open('../room_states.json', 'r') as file:
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

        await asyncio.sleep(diff_secs)

        with open('../room_states.json', 'r') as file:
            for line in file:
                room_states = json.loads(line)
                if room_id in room_states and room_states[room_id] == "stop":
                    print("Recording stopped for this room.")
                    return
            file.close()

        record_request(new_cameras_id)
        save_room_state(room_id, "recording")

        await asyncio.sleep(diff_secs)


@api.route('/')
class RecordStarter(Resource):
    @api.expect(record_model)
    def post(self):
        data = request.json
        room = Room(data['room_id'], data['cameras_id'])
        asyncio.run(record(room))
        return {'message': 'Recording started'}, 200

record_namespace = api

if __name__ == '__main__':
    from flask import Flask
    from flask_restx import Api

    app = Flask(__name__)
    api = Api(app)
    api.add_namespace(record_namespace)

    app.run(debug=True)
