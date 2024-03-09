import requests
import datetime
import asyncio
import os

address = 'http://51.250.23.237:8080'
trigger_url = address + '/7XNORkX7v3Sz9h3LldW39EYAYOZjX5/motion/1/%camera%?data={"plug":"Актовый зал","name":"Home-Assistant","reason":"TRY_TO_RECORD","confidence":100}'

monitor_url1 = address + '/7XNORkX7v3Sz9h3LldW39EYAYOZjX5/motion/1/krkvVjzAwf?data={"plug":"Актовый зал","name":"Home-Assistant","reason":"TRY_TO_RECORD","confidence":100}'

camera_url = address + '/7XNORkX7v3Sz9h3LldW39EYAYOZjX5/monitor/1/krkvVjzAwf'


class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id


rooms = [Room("abc", ["Ml2sBI1IQu"])]


def get_camera():
    try:
        response1 = requests.get(camera_url)
        if response1.status_code == 200:
            now1 = datetime.datetime.now()
            print(now1.time())
            print('Camera info')
            print(response1.json())
        else:
            print('GET request failed. Error:', response1.status_code)
    except Exception as e:
        print(f'Error stopping recording: {e}')


def trigger(cameras):
    for camera in cameras:
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


def change_audio(video_folder, audio_file):
    """
        Takes audio from specified video and pastes
        on specified videos list.

        Parameters
        ----------
        video_folder : str

        audio_file : str
            File name which audio should been applied.
    """
    for file in os.listdir(video_folder):
        if file.endswith('.mp4') or file.endswith('.avi') or file.endswith('.mkv'):
            video_path = os.path.join(video_folder, file)
            output_file = os.path.splitext(file)[0] + '_new.mp4'

            command = f'/opt/homebrew/bin/ffmpeg -i "{video_path}" -i "{audio_file}" -c:v copy -map 0:v:0 -map 1:0 "{output_file}"'
            os.system(command)


def join(folder):
    """
        Join all videos in folder to one.

        Parameters
        ----------
        folder : str
            Source folder path
    """
    # Получаем список всех видео файлов в папке
    video_files = [f for f in os.listdir(folder) if f.endswith('.mp4')]

    # Сортируем видео файлы по дате
    video_files.sort()

    # Создаем файл, в который будем записывать список видео файлов
    list_file_path = os.path.join(folder, 'list.txt')

    with open(list_file_path, 'w') as list_file:
        for video_file in video_files:
            list_file.write(f"file '{os.path.join(video_file)}'\n")

    # Получаем абсолютный путь к файлу list.txt
    abs_list_file_path = os.path.abspath(list_file_path)

    # Собираем команду для ffmpeg
    command = f"/opt/homebrew/bin/ffmpeg -y -f concat -i {abs_list_file_path} -c copy {os.path.join(folder, 'output.mp4')}"

    print(command)

    # Выполняем команду
    os.system(command)




async def record(minutes_to_record, room_id):
    """
        Record specified minutes from selected room

        If the argument `minutes_to_record` = -1 then video
        will be record while STOP command not entered.

        Parameters
        ----------
        minutes_to_record : int

        room_id : str
    """
    cameras_id = []
    print("Start recording")

    for room in rooms:
        if room.room_id == room_id:
            cameras_id = room.cameras_id

    while minutes_to_record > 0:
        trigger(cameras_id)
        await asyncio.sleep(64)
        minutes_to_record -= 1

    if minutes_to_record == -1:
        stop_recording = False
        while not stop_recording:
            for camera in cameras_id:
                trigger(camera)
            await asyncio.sleep(64)
            user_input = input("Enter 'STOP' to stop recording: ")
            if user_input == "STOP":
                stop_recording = True


async def main():
    await record(minutes_to_record=2, room_id="abc")
    #join("506")
    #change_audio("506", "506/2024-03-08T18-13-36.mp4")


if __name__ == '__main__':
    asyncio.run(main())
