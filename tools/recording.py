import asyncio
import cv2
import datetime
import os
import requests

address = ""
api_key = ""
group_key = ""


trigger_url = address + '/'+api_key+'/motion/'+group_key+'/%camera%?data={"plug":"Актовый зал","name":"Home-Assistant","reason":"TRY_TO_RECORD","confidence":100}'

monitor_url1 = address + '/'+api_key+'/motion/1/krkvVjzAwf?data={"plug":"Актовый зал","name":"Home-Assistant","reason":"TRY_TO_RECORD","confidence":100}'

camera_url = address + '/'+api_key+'/monitor/1/krkvVjzAwf'


class Room:
    def __init__(self, room_id, cameras_id):
        self.cameras_id = cameras_id
        self.room_id = room_id


rooms = [Room("abc", ["305_3"])]


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


def join(folder, room_id, placeholder):
    """
        Join all videos in folder to one.

        Parameters
        ----------
        folder : str
            Source folder path
        roomd_id : int
            ID of room
        placeholder : str
            Path to image for placeholder if video fragment is broken.
    """
    cameras_id = []
    print("Start joining")

    for room in rooms:
        if room.room_id == room_id:
            cameras_id = room.cameras_id
    for camera in cameras_id:

        # Получаем список всех видео файлов в папке
        video_files = [f for f in os.listdir(folder + '/' + camera) if f.endswith('.mp4')]

        # Сортируем видео файлы по дате
        video_files.sort()

        # Проверяем, есть ли битые или пропущенные видео
        for i in range(len(video_files)):
            video_path = os.path.join(folder, camera, video_files[i])
            if not os.path.exists(video_path):
                video_files[i] = placeholder
                print(f'Пропущенный файл: {video_path}')
            elif get_video_duration(video_path) < 50:
                video_files[i] = placeholder
                print(f'Битый файл: {video_path}')

        # Создаем файл, в который будем записывать список видео файлов
        list_file_path = os.path.join(folder + '/' + camera, 'list.txt')

        with open(list_file_path, 'w') as list_file:
            for video_file in video_files:
                list_file.write(f"file '{os.path.join(video_file)}'\n")

        # Получаем абсолютный путь к файлу list.txt
        abs_list_file_path = os.path.abspath(list_file_path)

        # Собираем команду для ffmpeg
        command = f"/opt/homebrew/bin/ffmpeg -y -f concat -i {abs_list_file_path} -c copy {os.path.join(folder + '/' + camera, 'output.mp4')}"

        print(command)

        # Выполняем команду
        os.system(command)


def get_video_duration(video_path):
    """
    Gets the duration of a video file.

    Args:
        video_path (path): Path to the video file.
    Returns:
        (int): Duration of the video file in seconds.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return -1     # Error opening the video file
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        return -1     # Error getting the FPS
    duration = length / fps
    cap.release()
    return duration




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
    room_id = "abc"
    minutes_to_record = 2
    folder = "/home/Shinobi/videos"
    main_audio_file = "/home/Shinobi/videos/test/main.mp4"

    await record(minutes_to_record=minutes_to_record, room_id=room_id)
    await asyncio.sleep(5)
    join(folder, room_id, 'NO_VIDEO.jpg')
    #change_audio(folder, main_audio_file)


if __name__ == '__main__':
    asyncio.run(main())
