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


def join(folder, room, placeholder):
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
    cameras_id = room.cameras_id
    print("Start joining")

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
        return -1  # Error opening the video file
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        return -1  # Error getting the FPS
    duration = length / fps
    cap.release()
    return duration


async def main():
    parser = argparse.ArgumentParser(description="Объединение видеозаписей")
    parser.add_argument("--placeholder", help="Путь к картинке 'Нет сигнала'", default="NO_VIDEO.jpg")

    parser.add_argument("--folder", help="Главная папка, в которой хранятся папки с записями",
                        default="/home/Shinobi/videos")
    parser.add_argument("--audio_file",
                        help="Путь к видео, аудиозапись которого необходимо наложить на остальные записи.",
                        default=None)

    args = parser.parse_args()
    join(args.folder, args.room, args.placeholder)
    if args.audio_file is not None:
        change_audio(args.room, args.audio_file)


if __name__ == '__main__':
    asyncio.run(main())
