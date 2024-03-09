# Документация
## Целевая аудитория
Основным заказчиком является Медиа центр МИЭМ, а так же другие медиа центры, которые хотят непрерывно записывать какие-либо комнаты с большим количеством камер и при этом с возможностью выбора аудио с одной из камер.

## Струтура проекта
* `lib` - весь основоной код API.
* `lib/ut` - тесты ручек и именно здесь нужно запускать тесты.
* `tools` - вспомогательные скрипты.

## Установка программы
Для работы с реализованным функционалом необходимо склонировать на устройство с характеристиками соотвествующие требования.

`git clone https://github.com/wtfthefirefox/sync-recording.git`

Переходим в папку проекта и запустаем скрипт для установки используемых пакетов.

`pip install -r requirements.txt`

Убеждаемся, что все тесты корректно работают:
1. `cd lib/ut`
2. `pytest`

## Добавление камер в shinobi
С помощью скрипта `tools/load_camera` возможно добавлять свои камеры с нужным конфигом.
Подробное описание каждого из параметров можно найти в документации к API Shinobi:
<https://docs.shinobi.video/api/add-edit-or-delete-a-monitor>

Пример вызова функции:

`load_camera(
    ip='http://your_ip:8080/',
    api='your_api',
    group=1,
    mid='monitor_id',
    name='monitor_name',
    host='ip_address',
    port='8080',
    auto_host='rtsp_address',
    detector='1', detector_trigger='1', detector_buffer_hls_time='5',
    detector_send_frames='0',
    detector_timeout='1'
)`

## Как запустить код?
1. Устанавливаем shinobi:
    1. `sudo su`(Ubuntu) или `su`(Mac OS, Centos)
    2. Следуем инструкции: `sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh)`
2. `python main.py --config-path your_path -u 8081`.

## А где в итоге все запускается?
Сама shinobi будет доступна на `http://your_ip:8080`, а апи доступна соотвественно на `http://your_ip:8081`.

## API
На данный момент доступна одна ручка `/download/file/{fileName}?dir_path={yourDirPath}`, где `fileName` это имя файла, который хотелось бы загрузить и `yourDirPath` это путь до папки в которой лежит файл и также это необязательный параметр.